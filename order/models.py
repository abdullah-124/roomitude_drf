from decimal import Decimal
from django.db import models
from account.models import User
from products.models import FurnitureProduct
# Create your models here.
STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

PAYMENT_METHODS = [
        ("cod", "Cash on Delivery"),
        ("card", "Credit/Debit Card"),
        ("bkash", "bKash"),
        ("paypal", "PayPal"),
    ]
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    # Billing / shipping info (can be copied from user profile at time of order)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Bangladesh")
    # Financials
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    shipping_method = models.CharField(max_length=20, default='standard')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    # Payment / status
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="cod")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    is_paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(FurnitureProduct, on_delete=models.PROTECT)  # assuming Product model exists
    
    # snapshot fields (price & name at time of purchase)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        if self.product_price is None or self.quantity is None:
            return Decimal("0.00")
        return self.product_price * self.quantity

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"