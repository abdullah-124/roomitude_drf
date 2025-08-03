from django.urls import path
from products.views import FurnitureProductView, ProductManageAPIView

urlpatterns = [
    path('', FurnitureProductView.as_view(), name='products_list'),
    path('<int:id>/', FurnitureProductView.as_view(), name='get_single_product'),
    path('manage/', ProductManageAPIView.as_view(), name='product_manage_view')
]