from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from products.models import FurnitureProduct
from products.serializers import FurnitureProductSerializer


# ALL PRODUCT VIEW WITH DEFAULT PAGINATION
class ProductView(GenericAPIView, ListModelMixin):
    serializer_class = FurnitureProductSerializer
    queryset = FurnitureProduct.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        categories = params.get('categories')
        if categories:
            categories_list = categories.split(',')
            qs = qs.filter(category__slug__in=categories_list).distinct()
        price_min = params.get('price_min')
        if price_min and price_min.isdigit():
            qs = qs.filter(price__gte=float(price_min))

        price_max = params.get('price_max')
        if price_max and price_max.isdigit():
            qs = qs.filter(price__lte=float(price_max))

        in_stock = params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            qs = qs.filter(stock_quantity__gt=0)

        tags = params.get('tags')
        if tags:
            tag_list = tags.split(',')
            qs = qs.filter(tags__slug__in=tag_list).distinct()

        # 'trending', 'best_sellers', 'featured', 'disscount'
        featured = params.get('featured')
        if featured and featured.lower() == 'true':
            qs = qs.filter(is_featured=True)
        discounted = params.get('discount')
        if discounted and discounted.lower() == 'true':
            qs = qs.filter(discount__gt = 0).order_by('-discount')
        trending = params.get('trending')
        if trending and trending.lower() == 'true':
            qs = qs.order_by('-views')
        best_sellers = params.get('best_sellers')
        if best_sellers and best_sellers.lower() == 'true':
            print('dd')
            qs = qs.order_by('-total_sales')
        category = params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        # Sorting
        sort = params.get('sortBy')
        sort_mapping = {
            'price_asc': '-price',
            'price_desc': 'price',
            'newest': '-created_at',
            'oldest': 'created_at',
            'best_sellers': '-total_sales',
            'rating': '-total_ratings',
        }
        if sort in sort_mapping:
            qs = qs.order_by(sort_mapping[sort])

        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# single product view
class SingleProductView(GenericAPIView, RetrieveModelMixin):
    queryset = FurnitureProduct.objects.all()
    serializer_class = FurnitureProductSerializer

    def get(self,req, pk):
        product = self.get_object()
        serializer = self.get_serializer(product)

        # Example: get related products by category (excluding the current one)
        related_products = FurnitureProduct.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:2]  # limit 2

        related_serializer = self.get_serializer(related_products, many=True)

        return Response({
            "product": serializer.data,
            "related_products": related_serializer.data,
        })
        
# PRODUCT SEARCH VIEW
class ProductSearchView(GenericAPIView, ListModelMixin):
    serializer_class = FurnitureProductSerializer
    queryset = FurnitureProduct.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        q = params.get('q')
        if q:
            qs = qs.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(category__name__icontains=q)
        )

        return qs
    
    def get(self, request, *args, **kwargs):    
        search_result = self.get_queryset()[:5]
        products = self.serializer_class(search_result, many=True, context={'request': request})
        return Response({'result': products.data})