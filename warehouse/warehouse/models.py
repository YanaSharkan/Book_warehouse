from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brief_description = models.CharField(max_length=300, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title


class BookItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='items')
    place = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    user_email = models.EmailField()
    ORDER_STATUS = (
        ('w', 'In work'),
        ('s', 'Success'),
        ('f', 'Fail'),
    )
    status = models.CharField(
        max_length=1,
        choices=ORDER_STATUS,
        blank=True,
        default='w',
    )
    delivery_address = models.CharField(max_length=250)
    order_id_in_shop = models.IntegerField()

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.id)
