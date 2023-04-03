from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from .views import BookViewSet, BookItemViewSet, OrderViewSet, OrderItemViewSet, OrderItemBookItemViewSet


router = routers.DefaultRouter()
router.register(r'book', BookViewSet)
router.register(r'book_item', BookItemViewSet)
router.register(r'order', OrderViewSet)
router.register(r'order_item', OrderItemViewSet)
router.register(r'order_item_book_item', OrderItemBookItemViewSet)


app_name = 'warehouse'
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]