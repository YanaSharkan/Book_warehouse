from django.contrib import admin

from .models import Book, BookItem, Order, OrderItem, OrderItemBookItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'brief_description', 'description')
    fields = ('title', 'price', 'brief_description', 'description')
    search_fields = ('title',)


@admin.register(BookItem)
class BookItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'place')
    fields = ('book_id', 'place')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_email', 'status', 'delivery_address', 'order_id_in_shop')
    fields = ('user_email', 'status', 'delivery_address', 'order_id_in_shop')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'book_store_id', 'quantity')
    fields = ('order', 'book_store_id', 'quantity')


@admin.register(OrderItemBookItem)
class OrderItemBookItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_item', 'book_item')
    fields = ('order_item', 'book_item')



