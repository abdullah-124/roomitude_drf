from django.db import models
from account.models import User
from products.models import FurnitureProduct

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(FurnitureProduct, on_delete=models.CASCADE, related_name='wishlist_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']
        verbose_name = 'Wishlist Item'
        verbose_name_plural = 'Wishlist Items'