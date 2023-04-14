import json

from celery import shared_task
from celery.schedules import timedelta

from core.celery import app

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

import requests


from .models import Book, Order

User = get_user_model()


@shared_task()
def send_order_created(email, user_email):
    send_mail(
        'New order was created',
        'New order was created by user {0}'.format(user_email),
        'user@store.com',
        email,
        fail_silently=False,
    )


@app.task
def get_books():
    books_r = requests.get(f'{settings.BASE_URL}/book/')
    books_json = json.loads(books_r.content)
    books_l = books_json['results']

    for book in books_l:
        try:
            book_m = Book.objects.get(warehouse_id=book['id'])
            book_m.price = book['price']
            book_m.quantity = len(book['items'])
            book_m.brief_description = book['brief_description']
            book_m.description = book['description']
            book_m.save()
        except Book.DoesNotExist:
            Book.objects.create(title=book['title'], warehouse_id=book['id'],
                                price=book['price'], quantity=len(book['items']),
                                brief_description=book['brief_description'], description=book['description'])


@app.task
def update_orders():
    orders_r = requests.get(f'{settings.BASE_URL}/order/')
    orders_json = json.loads(orders_r.content)
    warehouse_orders = orders_json['results']
    store_orders = Order.objects.all()
    superusers_emails = User.objects.filter(is_superuser=True).values_list('email').first()

    for store_order in store_orders:
        warehouse_entry = list(filter(lambda order: order['order_id_in_shop'] == store_order.id, warehouse_orders))
        if len(warehouse_entry) == 0:  # Check that order exists in warehouse
            order_param = {"user_email": store_order.user.email,
                           "status": "w",
                           "delivery_address": store_order.delivery_address,
                           "order_id_in_shop": store_order.id}
            create_order_r = requests.post(f'{settings.BASE_URL}/order/', order_param)
            warehouse_order = json.loads(create_order_r.content)  # Get created order from warehouse
            order_items = store_order.orderitem_set.all()
            for order_item in order_items:
                order_item_param = {"book": order_item.book.warehouse_id,
                                    "order": warehouse_order["id"],
                                    "quantity": order_item.quantity}
                requests.post(f'{settings.BASE_URL}/order_item/', order_item_param)  # Create order item in warehouse
        elif warehouse_entry[0]['status'] != 'w':  # Order status changed in warehouse
            if warehouse_entry[0]['status'] == 's' and store_order.status != 's':
                send_mail(
                    'Order was completed',
                    'Order with id {0} was complete'.format(store_order.id),
                    'user@store.com',
                    superusers_emails,
                    fail_silently=False,
                )
            store_order.status = warehouse_entry[0]['status']
            store_order.save()


app.conf.beat_schedule = {
    'books': {
        'task': 'store.tasks.get_books',
        "schedule": timedelta(seconds=3)
    },
    'orders': {
        'task': 'store.tasks.update_orders',
        'schedule': timedelta(seconds=3)
    }
}
