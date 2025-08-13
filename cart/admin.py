from django.contrib import admin
from cart import models
# Register your models here.

@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id','user','user__first_name','product','quantity',]
