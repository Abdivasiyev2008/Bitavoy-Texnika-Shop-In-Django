from django.urls import path
from .views import *

urlpatterns = [
    path('', homePage, name='home'),
    path('shop/', shop, name='shop'),
    path('item-list/<int:pk>/', itemList, name='item-list'),
    path('order-list/<int:pk>/', orderlist, name='order-list'),
    path('order-detail/<int:pk>/', orderDetail, name='order-detail'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('remove_from_cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('add_to_favorites/<int:pk>/', add_to_favorites, name='add_to_favorites'),
    path('favorite/', favorite, name='favorite'),
    path('remove_from_favorite/<int:pk>/', remove_from_favorite, name='remove_from_favorite'),
    path('check-out/', checkout, name='check-out'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),

    ############## About Shop
    path('about/', about, name='about'),
    path('questions/', questions, name='questions'),
]