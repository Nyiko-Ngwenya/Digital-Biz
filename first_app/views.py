from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# from .forms import
# Create your views here.


def home(request):
    return render(request, 'first_app/index.html')


def accounts(request):
    return render(request, 'first_app/accounts.html')

def logoutPage(request):
    logout(request)
    return redirect('loginPage')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username , password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is wrong')
    context = {}
    return render(request, 'first_app/login.html', context)


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,f'The user {user} was created')
            return redirect('login')
    context = {'form': form}
    return render(request, 'first_app/register.html',context)