from django.urls import path
from category.views import CategoryView, ProductByCategory
urlpatterns = [
    path('', CategoryView.as_view(), name='category_list'),
    path('<str:slug>/', ProductByCategory.as_view(), name='product_by_category')
]
