from django.db import models
from django.utils.text import slugify

from brand.models import Brand
from category.models import Category

# Create your models here.
class FurnitureProduct(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.FloatField( blank=True, null=True, help_text="Enter discount as a percentage (e.g., 10 for 10%)" )
    in_stock = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    materials = models.TextField()
    dimensions = models.CharField(max_length=100, help_text="Format: L x W x H in cm")
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="kg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            while FurnitureProduct.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_price(self):
        if self.discount:
            return round(self.price * (1 - self.discount / 100), 2)
        return self.price
