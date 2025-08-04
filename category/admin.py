from django.contrib import admin
from category import models
# Register your models here.

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug','image']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']
    list_editable = ['image']
    ordering = ['id']