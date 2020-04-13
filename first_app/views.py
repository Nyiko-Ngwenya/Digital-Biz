from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'first_app/index.html')


def accounts(request):
    return render(request, 'first_app/accounts.html')


def login(request):
    return render(request, 'first_app/login.html')


def register(request):
    return render(request, 'first_app/register.html')