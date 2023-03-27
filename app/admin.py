from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Coustomer)
class CoustomerAdmin(admin.ModelAdmin):
    list_display=['id','name','locality','city','zipcode','state']
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discount_price','description','brand','category','product_image']
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
    
@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','order_date','status']