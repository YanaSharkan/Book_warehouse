from rest_framework import viewsets

from .models import Book, BookItem, Order, OrderItem
from .serializers import BookItemViewSetSerializer, BookViewSetSerializer, OrderItemViewSetSerializer, OrderViewSetSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related('items').all()
    serializer_class = BookViewSetSerializer


class BookItemViewSet(viewsets.ModelViewSet):
    queryset = BookItem.objects.select_related('book').all()
    serializer_class = BookItemViewSetSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderViewSetSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order').all()
    serializer_class = OrderItemViewSetSerializer
