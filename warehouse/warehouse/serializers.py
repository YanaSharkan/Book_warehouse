from rest_framework import serializers

from .models import Book, BookItem, Order, OrderItem


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
    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'order', 'quantity']
