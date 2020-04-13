from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts', views.accounts, name='accounts'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login')
]
