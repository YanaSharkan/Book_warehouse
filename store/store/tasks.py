import json
import requests

from celery.schedules import timedelta
from core.celery import app

from .models import Book


@app.task
def get_books():
    base_url = 'http://127.0.0.1:8001/warehouse'
    books_r = requests.get(f'{base_url}/book/')
    books_json = json.loads(books_r.content)
    books_l = books_json['results']

    for book in books_l:
        try:
            book_m = Book.objects.get(title=book['title'])
            book_m.price = book['price']
            book_m.quantity = len(book['items'])
            book_m.brief_description = book['brief_description']
            book_m.description = book['description']
            book_m.save()
        except Book.DoesNotExist:
            Book.objects.create(title=book['title'], price=book['price'], quantity=len(book['items']),
                                brief_description=book['brief_description'], description=book['description'])


app.conf.beat_schedule = {
    'scraping': {
        'task': 'store.tasks.get_books',
        "schedule": timedelta(seconds=3)
    }
}