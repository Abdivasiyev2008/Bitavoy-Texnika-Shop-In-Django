from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class Item(models.Model):
    image = models.ImageField(upload_to='images/item/')
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    image = models.ImageField(upload_to='images/order-item/')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    orderItem = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    about = RichTextField()
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class OrderImage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='order/images/')

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product} - {self.quantity}'
    
class CheckOut(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.user} - {self.email} - {self.phone}'

class CheckOutUser(models.Model):
    order = models.ForeignKey(CheckOut, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.order} - {self.quantity}'

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    text = models.TextField()

    def __str__(self):
        return str(self.user)
    
class FavoriteItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product}'