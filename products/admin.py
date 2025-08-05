from django.contrib import admin
from products.models import FurnitureProduct
# Register your models here.
@admin.register(FurnitureProduct)
class FurnitureProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','discount', 'image']
    list_editable = ['image']