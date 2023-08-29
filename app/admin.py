from django.contrib import admin
from .models import *

# Register your models here.
# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = OrderImage


class CheckOutUserInline(admin.TabularInline):
    model = CheckOutUser

###################################################

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

class CheckOutUserAdmin(admin.ModelAdmin):
    inlines = [CheckOutUserInline]

###################################################

admin.site.register(OrderImage)
admin.site.register(Order, ProductAdmin)
admin.site.register(OrderItem)
admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(FavoriteItem)
admin.site.register(Contact)
admin.site.register(CheckOut, CheckOutUserAdmin)