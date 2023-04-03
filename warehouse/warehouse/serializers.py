from rest_framework import serializers

from .models import Book, BookItem, Order, OrderItem, OrderItemBookItem


# Serializers define the API representation.
class BookViewSetSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'items', 'price', 'brief_description', 'description']


class BookItemViewSetSerializer(serializers.ModelSerializer):
    book = BookViewSetSerializer(read_only=True)

    class Meta:
        model = BookItem
        fields = ['id', 'book', 'place']


class OrderViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user_email', 'status', 'delivery_address', 'order_id_in_shop']


class OrderItemViewSetSerializer(serializers.ModelSerializer):
    order = OrderViewSetSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'book_store_id', 'quantity']


class OrderItemBookItemViewSetSerializer(serializers.ModelSerializer):
    order_item = OrderItemViewSetSerializer(read_only=True)
    book_item = BookItemViewSetSerializer(read_only=True)

    class Meta:
        model = OrderItemBookItem
        fields = ['id', 'order_item', 'book_item']
