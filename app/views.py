from django.shortcuts import render, redirect, get_object_or_404
from .models import *
import numpy as np
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit

# Create your views here.

def homePage(request):
    item = Item.objects.all()
    order = Order.objects.all()
    orederitem = OrderItem.objects.all()
    fr_cr = np.random.choice(order, size=1, replace=False)
    twice_cr = np.random.choice(order, size=2, replace=False)

    context = {
        'item': item,
        'order': order,
        'orederitem': orederitem,
        'fr_cr': fr_cr,
        'twice_cr': twice_cr,
    }

    return render(request, 'index.html', context)

def itemList(request, pk):
    item = Item.objects.all().filter(id=pk)
    item_list = OrderItem.objects.all().filter(id=pk)
    orederitem = OrderItem.objects.all().filter(id=pk)
    
    order = Order.objects.all()
    order = np.random.choice(order, size=2, replace=False)
    
    context = {
        'item': item,
        'list': item_list,
        'order': order,
        'orederitem': orederitem,
    }

    return render(request, 'item_list.html', context)

def orderlist(request, pk):
    item = Item.objects.all().filter(id=pk)
    orederitem = OrderItem.objects.all().filter(id=pk)
    list = Order.objects.all().filter(orderItem=pk)
    order = Order.objects.all()
    order = np.random.choice(order, size=2, replace=False)
    
    context = {
        'item': item,
        'list': list,
        'order': order,
        'orederitem': orederitem,
        'list': list,
    }

    return render(request, 'order-list.html', context)

def orderDetail(request, pk):
    detail = Order.objects.get(id=pk)
    orederitem = OrderItem.objects.all()
    item = Item.objects.all()
    order = Order.objects.all()
    order = np.random.choice(order, size=2, replace=False)
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    
    else:
        cart_items = ""

    order = np.random.choice(order, size=2, replace=False)

    context = {
        'item': item,
        'detail': detail,
        'order': order,
        'orederitem': orederitem,
        'cart_items': cart_items,
    }

    return render(request, 'detail.html', context)

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total_price = 0

    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        total_price += item.total_price

    orederitem = OrderItem.objects.all()
    item = Item.objects.all()
    order = Order.objects.all()
    order = np.random.choice(order, size=2, replace=False)
    
    order = np.random.choice(order, size=2, replace=False)

    context = {
        'item': item,
        'order': order,
        'orederitem': orederitem,
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Order, id=pk)
    action = request.POST.get('action')
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
    )

    if int(cart_item.quantity) > 0:
        if not created:
            if action == 'plus':
                cart_item.quantity += 1
            
            elif action == 'minus' and cart_item.quantity > 1:
                cart_item.quantity -= 1

    cart_item.save()
    referring_page = request.META.get('HTTP_REFERER')
    
    return HttpResponseRedirect(referring_page)

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, id=pk)
    item.delete()
    # Qaytish yoki sahifaga yonlashingiz kerak bo'lsa:

    referring_page = request.META.get('HTTP_REFERER')
    
    return HttpResponseRedirect(referring_page)

@login_required
def add_to_favorites(request, pk):
    product = get_object_or_404(Order, id=pk)
    favorite_item = FavoriteItem(user=request.user, product=product)
    favorite_item.save()

    referring_page = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referring_page)

@login_required
def favorite(request):
    favorite_items = FavoriteItem.objects.filter(user=request.user)
    item = Item.objects.all()

    context = {
        'item': item,
        'favorite_items': favorite_items,
    }

    return render(request, 'favorite.html', context)

@login_required
def remove_from_favorite(request, pk):
    item = get_object_or_404(FavoriteItem, id=pk)
    item.delete()
    # Qaytish yoki sahifaga yonlashingiz kerak bo'lsa:

    referring_page = request.META.get('HTTP_REFERER')
    
    return HttpResponseRedirect(referring_page)


@login_required
def checkout(request):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('home')

    total = 0
    quantity = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    if request.method == 'POST':
        if request.POST['phone'] == '' or request.POST['address1'] == '' or request.POST['address2'] == '' or request.POST['state'] == '' or request.POST['city'] == '':
            return redirect('check-out')
        
        else:
            data = CheckOut()
            data.user = current_user
            data.first_name = request.user.first_name
            data.last_name = request.user.last_name
            data.phone = request.POST['phone']
            data.email = request.user.email
            data.address1 = request.POST['address1']
            data.address2 = request.POST['address2']
            data.state = request.POST['state']
            data.city = request.POST['city']
            data.save()

            for cart_item in cart_items:
                checkout_user = CheckOutUser()
                checkout_user.order = data
                checkout_user.user = current_user
                checkout_user.product = cart_item.product
                checkout_user.product_price = cart_item.product.price
                checkout_user.quantity = cart_item.quantity
                checkout_user.ordered = False
                checkout_user.save()

            cart_items.delete()  # Remove the purchased items from CartItem
    
    item = Item.objects.all()

    context = {
        'cart_items': cart_items,
        'total': total,
        'item': item,
    }
    
    return render(request, 'checkout.html', context)

@ratelimit(key='user_or_ip', rate='3/m')
@login_required
def contact(request):
    if request.method == "POST":
        Contact.objects.get_or_create(
            user = request.user,
            first_name = request.user.first_name,
            last_name = request.user.last_name,
            email = request.user.email,
            text = request.POST["text"],
        )
        
        referring_page = request.META.get('HTTP_REFERER')
        
        return HttpResponseRedirect(referring_page)
    
    item = Item.objects.all()
    context = {
        'item': item,
    }

    return render(request, "contact.html", context)

def shop(request):
    order = Order.objects.all()
    item = Item.objects.all()
    
    context = {
        'item': item,
        'order': order,
    }
    return render(request, 'shop.html', context)

def search(request):
    item = Item.objects.all()
    
    if 'q' in request.GET:
        q = request.GET['q']
        order = Order.objects.filter(name__icontains=q)

    else:
        order = Order.objects.all()

    context = {
        'item': item,
        'order': order,
    }

    return render(request, 'search.html', context)


######################## About Shop ########################

def about(request):
    return render(request, 'about_shop/about.html')

def questions(request):
    return render(request, 'about_shop/questions.html')


##################################### HTTP Errors ###############################

def error_404(request, exception=None):
    return render(request, 'error/404.html')

def error_403(request, exception=None):
    return render(request, 'error/403.html')

def error_500(request, exception=None):
    return render(request, 'error/500.html')