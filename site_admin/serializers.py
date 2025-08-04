from rest_framework import serializers
from account.models import User
from products.serializers import FurnitureProduct
from category.serializers import CategorySerializer

class UserSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
# product serializer 

class FurnitureSerializerAdmin(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested serializer
    class Meta:
        model = FurnitureProduct
        fields = '__all__'