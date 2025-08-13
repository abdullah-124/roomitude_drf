from django.db import models
from django.utils.text import slugify
from decimal import Decimal, ROUND_HALF_UP
from brand.models import Brand
from category.models import Category



# Create your models here.
# TAG MODEL FOR PRODUCT 
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        slug = self.slug
        print('user',slug)
        if(not slug):
            slug = slugify(self.name)
            self.slug = slug
            print('after slugify', slug)
        existing = Tag.objects.filter(slug=slug).first()
        if existing:
            # If exists, update current instance to match the existing one
            self.id = existing.id  # this makes save() do an update instead of insert
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

# FURNITURE PRODUCT MODEL 
class FurnitureProduct(models.Model):
    # basic information
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    short_description = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    # price and stock
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.FloatField( blank=True, null=True, help_text="Enter discount as a percentage (e.g., 10 for 10%)" )
    in_stock = models.BooleanField(default=True)
    # taging
    tags = models.ManyToManyField(Tag, blank=True)
    # basic filtering
    stock_quantity = models.PositiveIntegerField(default=0)
    materials = models.TextField()
    dimensions = models.CharField(max_length=100, help_text="Format: L x W x H in cm")
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="kg")
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(null=True, blank=True)
    total_sales = models.PositiveIntegerField(null=True, blank=True)
    total_review = models.PositiveIntegerField(null=True,blank=True)
    total_ratings = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ordering
    class Meta:
        ordering = ['-created_at']

    # slugify when any of product has created
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
    # representation
    def __str__(self):
        return self.name

    # calculate exact price with discount
    def get_price(self):
        if self.discount:
            discount_fraction = Decimal(1) - (Decimal(self.discount) / Decimal(100))
            discounted_price = self.price * discount_fraction
            # Round to 2 decimal places with decimal rounding
            return discounted_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return self.price
    # calculate ratings
    def get_rating(self):
        if(self.total_review and self.total_ratings):
            return round(self.total_ratings/self.total_review, 1)
        return 0.0
