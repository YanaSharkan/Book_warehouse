from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from store.forms import RegisterForm

from .models import Book, Order, OrderItem, Profile
from .tasks import send_order_created

User = get_user_model()


class MainView(generic.ListView):
    template_name = 'store/main.html'
    context_object_name = 'entries_list'
    paginate_by = 10
    model = Book

    def get_queryset(self):
        return Book.objects.all()


class CartView(generic.ListView):
    template_name = 'store/cart.html'
    context_object_name = 'entries_list'
    model = OrderItem

    def get_queryset(self):
        try:
            cart_order = Order.objects.get(user=self.request.user, status='c')
            return OrderItem.objects.filter(order=cart_order).all()
        except Order.DoesNotExist:
            return []


class BookDetailsView(generic.DetailView):
    model = Book
    context_object_name = 'entry'
    template_name = "store/book.html"

    def get_object(self, queryset=None):
        book = Book.objects.get(id=self.kwargs["pk"])
        return book


def add_to_cart(request, pk):
    if request.user.is_anonymous:
        return redirect(reverse_lazy('store:login'))
    if not request.user.profile:
        return redirect(reverse_lazy('store:update_profile'))
    book = Book.objects.get(id=pk)
    try:
        cart_order = Order.objects.get(user=request.user, status='c')
    except Order.DoesNotExist:
        cart_order = Order.objects.create(user=request.user, status='c',
                                          delivery_address=request.user.profile.delivery_address)
    try:
        book_item = OrderItem.objects.get(book=book, order=cart_order)
        book_item.quantity = book_item.quantity + 1
        book_item.save()
    except OrderItem.DoesNotExist:
        OrderItem.objects.create(book=book, quantity=1, order=cart_order)

    messages.add_message(request, messages.SUCCESS, 'Product added to cart.')
    return redirect(reverse_lazy('store:cart'))


def remove_from_cart(request, pk):
    if request.user.is_anonymous:
        return redirect(reverse_lazy('store:login'))

    OrderItem.objects.filter(id=pk).delete()
    messages.add_message(request, messages.SUCCESS, 'Product was removed from cart.')
    return redirect(reverse_lazy('store:cart'))


def clean_cart(request):
    if request.user.is_anonymous:
        return redirect(reverse_lazy('store:login'))

    Order.objects.filter(user=request.user, status='c').delete()
    messages.add_message(request, messages.SUCCESS, 'Cart was cleared.')
    return redirect(reverse_lazy('store:cart'))


def complete_order(request):
    if request.user.is_anonymous:
        return redirect(reverse_lazy('store:login'))

    cart_order = Order.objects.get(user=request.user, status='c')
    cart_order.status = 'o'
    cart_order.save()
    superusers_emails = User.objects.filter(is_superuser=True).values_list('email').first()
    send_order_created.apply_async((superusers_emails, request.user.email))
    messages.add_message(request, messages.SUCCESS, 'Order created!')
    return redirect(reverse_lazy('store:cart'))


class RegisterFormView(SuccessMessageMixin, generic.FormView):
    template_name = "store/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("store:main")
    success_message = "User created"

    def form_valid(self, form):
        user = form.save()
        user = authenticate(self.request, username=user.username, password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Profile
    fields = ["delivery_address"]
    template_name = "store/update_profile.html"
    login_url = reverse_lazy('store:login')
    success_url = reverse_lazy("store:cart")
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        obj, created = Profile.objects.get_or_create(user=self.request.user)
        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UpdateProfile, self).form_valid(form)
