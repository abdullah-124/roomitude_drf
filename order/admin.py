from django.contrib import admin

# Register your models here.
from django.contrib import admin
from order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):  # or admin.StackedInline
    model = OrderItem
    extra = 0  # don't show extra blank forms
    readonly_fields = ("product_name", "product_price", "quantity", "get_total_price")

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = "Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "payment_method", "is_paid", "total", "created_at")
    list_filter = ("status", "payment_method", "is_paid", "created_at")
    search_fields = ("id", "user__username", "user__email", "transaction_id")
    readonly_fields = ("sub_total", "discount", "tax", "shipping_cost", "total", "created_at", "updated_at")

    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_name", "product_price", "quantity", "get_total_price")
    search_fields = ("product_name", "order__id")
    readonly_fields = ("product_name", "product_price", "quantity", "order")

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = "Total"
