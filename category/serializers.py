from rest_framework import serializers
from category.models import Category

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']


class CategoryWithCountSerializer(CategorySerializer):
    product_count = serializers.IntegerField()
    class Meta:
        model = Category
        fields = CategorySerializer.Meta.fields + ['product_count']