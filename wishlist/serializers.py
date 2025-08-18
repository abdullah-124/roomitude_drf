from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from wishlist.models import Wishlist
from products.serializers import FurnitureProductSerializer

class WishlistSerializer(ModelSerializer):
    product = FurnitureProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    class Meta: 
        model = Wishlist
        exclude = ['user']