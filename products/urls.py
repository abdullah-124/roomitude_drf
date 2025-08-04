from django.urls import path
from products.views import ProductView


urlpatterns = [
    path('', ProductView.as_view(), name='products'),
    path('<int:pk>', ProductView.as_view(), name='get_product')
]