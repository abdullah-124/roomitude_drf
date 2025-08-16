from django.contrib import admin
from wishlist.models import Wishlist
# Register your models here.

@admin.register(Wishlist)
class WishlistAdminView(admin.ModelAdmin):
    list_display = ['product', 'user', ]