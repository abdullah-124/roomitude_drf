from rest_framework.views import APIView
from rest_framework.response import Response
from category.models import Category
from category.serializers import CategorySerializer
from products.serializers import FurnitureProductSerializer


# Create your views here.
class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

class ProductByCategory(APIView):
    def get(self,request, slug, *args, **kwargs):
        category = Category.objects.get(slug=slug)
        products = category.products.all()
        serializer = FurnitureProductSerializer(products, many=True)
        return Response(serializer.data, *args, **kwargs)