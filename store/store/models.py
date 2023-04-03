from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    brief_description = models.CharField(max_length=300, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    ORDER_STATUS = (
        ('c', 'Cart'),
        ('o', 'Ordered'),
        ('s', 'Success'),
        ('f', 'Fail'),
    )
    status = models.CharField(
        max_length=1,
        choices=ORDER_STATUS,
        blank=True,
        default='c',
    )
    delivery_address = models.CharField(max_length=250)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.id)
