from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


app_name = 'store'
urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('book/<int:pk>/', views.BookDetailsView.as_view(), name='book'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout'),
    path('register/', views.RegisterFormView.as_view(), name='register'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart-remove/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('cart-clean/', views.clean_cart, name='clean_cart'),
    path('cart-complete/', views.complete_order, name='complete_order'),
    path("update_profile/", views.UpdateProfile.as_view(), name="update_profile"),
]
