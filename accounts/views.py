from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import *
from app.models import Item, CartItem
from django.contrib.auth import logout

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)  # Kirish

            return redirect('home')
    else:
        form = RegisterForm()
    
    item = Item.objects.all()
    return render(request, 'accounts/register.html', {'form': form, 'item': item})

def login_view(request):
    item = Item.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'Foydalanuvchi nomi yoki paroli noto\'g\'ri.')
            return redirect('login')
    
    return render(request, 'accounts/login.html', {'item': item})

def logout_view(request):
    logout(request)
    
    return redirect('home')
