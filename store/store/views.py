from store.forms import RegisterForm

from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page
from django.views.generic.edit import CreateView

from .models import Book, Order, OrderItem


class MainView(generic.TemplateView):
    template_name = 'store/main.html'


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
