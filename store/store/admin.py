from django.contrib import admin

from .models import Book, Order, OrderItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'quantity', 'brief_description', 'description')
    fields = ('title', 'price', 'quantity', 'brief_description', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'delivery_address')
    fields = ('status', 'delivery_address')


@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'book', 'quantity')
    fields = ('order', 'book', 'quantity')


