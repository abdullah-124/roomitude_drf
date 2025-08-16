from rest_framework.serializers import ModelSerializer
from wishlist.models import Wishlist
from products.serializers import FurnitureProductSerializer

class WishlistSerializer(ModelSerializer):
    product = FurnitureProductSerializer(read_only=True)
    class Meta: 
        model = Wishlist
        fields = '__all__'