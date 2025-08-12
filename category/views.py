# django 
from django.db.models import Count
# restframework
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
# local
from category.models import Category
from category.serializers import CategoryWithCountSerializer
from products.serializers import FurnitureProductSerializer


# Create your views here.
class CategoryView(ListAPIView):  # ✅ ListAPIView automatically supports GET
    pagination_class = None
    serializer_class = CategoryWithCountSerializer

    def get_queryset(self):
        return Category.objects.annotate(
            product_count=Count("products")
        )

class ProductByCategory(APIView):
    def get(self,request, slug, *args, **kwargs):
        category = Category.objects.get(slug=slug)
        products = category.products.all()
        serializer = FurnitureProductSerializer(products, many=True)
        return Response(serializer.data, *args, **kwargs)