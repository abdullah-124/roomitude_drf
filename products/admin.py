from django.contrib import admin
from products.models import FurnitureProduct, Tag
from django.utils.html import format_html
# Register your models here.

@admin.register(FurnitureProduct)
class FurnitureProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','discount','image_tag', 'image','is_featured' ]
    list_editable = ['image', 'discount', 'is_featured']
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

admin.site.register(Tag)