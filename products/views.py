from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from products.models import FurnitureProduct
from products.serializers import FurnitureProductSerializer


# ALL PRODUCT VIEW WITH DEFAULT PAGINATION
class ProductView(GenericAPIView, ListModelMixin):
    serializer_class = FurnitureProductSerializer
    queryset = FurnitureProduct.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        category = params.get('category')
        if category:
            qs = qs.filter(category__slug=category)

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

        rating_min = params.get('rating_min')
        if rating_min:
            try:
                rating_min_float = float(rating_min)
                qs = qs.filter(average_rating__gte=rating_min_float)
            except ValueError:
                pass

        featured = params.get('featured')
        if featured and featured.lower() == 'true':
            qs = qs.filter(is_featured=True)

        discounted = params.get('discounted')
        if discounted and discounted.lower() == 'true':
            qs = qs.filter(discount_price__lt=0)

        # Sorting
        sort = params.get('sort')
        sort_mapping = {
            'price_asc': 'price',
            'price_desc': '-price',
            'newest': '-created_at',
            'oldest': 'created_at',
            'best_sellers': '-total_sales',
            'rating': '-rating',
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
        return self.retrieve(req, pk=pk)