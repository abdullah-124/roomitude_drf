from rest_framework import serializers
from products.models import FurnitureProduct, Tag
from category.serializers import CategorySerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

# PRODUCT SERIALIZER
class FurnitureProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested serializer
    tags = TagSerializer(many=True)
    exact_price = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    class Meta:
        model = FurnitureProduct
        fields = '__all__'
    def get_exact_price(self, obj):
        return obj.get_price()
    def get_rating(self, obj):
        return obj.get_rating()