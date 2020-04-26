from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('accounts', views.accounts, name='accounts'),
    path('register', views.register, name='register'),
    path('login', views.loginPage, name='loginPage'),
    path('logout',views.logoutPage,name='logoutPage'),
    path('invoices',views.invoices,name='invoices'),
    path('budget', views.project_list, name = 'project_list'),
    path('add', views.ProjectCreateView.as_view(), name = 'add'),
    path('<slug:project_slug>', views.project_detail, name ='detail'),

]
