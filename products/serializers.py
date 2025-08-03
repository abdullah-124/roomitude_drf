from rest_framework import serializers
from products.models import FurnitureProduct
from category.serializers import CategorySerializer

class FurnitureProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested serializer
    class Meta:
        model = FurnitureProduct
        fields = '__all__'