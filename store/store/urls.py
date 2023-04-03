from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


app_name = 'store'
urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout'),
    path('register/', views.RegisterFormView.as_view(), name='register'),

]