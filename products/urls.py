from django.urls import path
from products.views import ProductView, SingleProductView, ProductSearchView


urlpatterns = [
    path('', ProductView.as_view(), name='products'),
    path('search/', ProductSearchView.as_view(), name='search_products'),
    path('<int:pk>/', SingleProductView.as_view(), name='get_product')
]