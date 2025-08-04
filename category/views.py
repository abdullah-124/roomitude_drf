from rest_framework.views import APIView
from rest_framework.response import Response
from category.models import Category
from category.serializers import CategorySerializer
from products.serializers import FurnitureProductSerializer


# Create your views here.
class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()   
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, *args, **kwargs)

class ProductByCategory(APIView):
    def get(self,request, slug, *args, **kwargs):
        category = Category.objects.get(slug=slug)
        products = category.products.all()
        serializer = FurnitureProductSerializer(products, many=True)
        return Response(serializer.data, *args, **kwargs)