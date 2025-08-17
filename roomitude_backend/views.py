import json
import random
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.core.cache import cache
from django.db.models import F, FloatField, ExpressionWrapper
# restframework 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# local 
from category.models import Category
from category.serializers import CategoryWithCountSerializer
from products.models import FurnitureProduct
from products.serializers import FurnitureProductSerializer
from account.models import User
from account.serializers import UserSerializer
from cart.models import CartItem
from cart.serializers import CartItemSerializer
from wishlist.models import Wishlist
from wishlist.serializers import WishlistSerializer
from roomitude_backend.data import products



def my_function(req):
  if(req.user.is_authenticated and req.user.username == 'admin'):
    f = FurnitureProduct.objects.values()
    data = list(f)
    return JsonResponse(data, safe=False)

  return HttpResponse('you do not have the permission to run this page 404 unauthorized')

class HomePageDataView(APIView):
  permission_classes = [IsAuthenticatedOrReadOnly]
  def get(self, request):
    response_data = {}
    try:
      response_data['categories'] = self.get_categories()
      response_data['products'] = self.get_products()
      response_data['user'] = self.get_user()
      response_data['cart'] = self.get_cart()
      response_data['wishlist'] = self.get_wishlist()
      return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e: 
      return Response({
          'success': False,
          'error': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # user info
  def get_user(self):
    if(self.request.user.is_authenticated):
      user = User.objects.get(username=self.request.user.username)
      data = UserSerializer(user, many=False).data
      return data
    return {}
  # cart info
  def get_cart(self):
    user = self.request.user
    if(user.is_authenticated):
      cartModel = CartItem.objects.filter(user=user)
      cart_items = CartItemSerializer(cartModel, many=True, context={'request': self.request})
      return cart_items.data
    return []
  # wishlist info
  def get_wishlist(self):
    user = self.request.user
    if(user.is_authenticated):
      wishlistModel = Wishlist.objects.filter(user=user)
      wishlist = WishlistSerializer(wishlistModel, many=True)
      return wishlist.data
    return []
  # categories
  def get_categories(self):
    cache_key = 'home_categories'
    cached = cache.get(cache_key)
    if cached:
        return cached
    try:
      categoriesModel = Category.objects.annotate(product_count=Count("products") )
      categories = CategoryWithCountSerializer(categoriesModel, many=True)
      data = categories.data
      cache.set(cache_key, data, 600)  # 10 minutes
      return data
    except Exception as e: 
      print('error', str(e))
      return []
    

  # GET PRODUCTS FOR HOME PAGE 
  def get_products(self):
    cache_key = 'home_products'
    cached = cache.get(cache_key)
    if(cached): 
      return cached
    try:
      queryset = FurnitureProduct.objects.filter(in_stock=True, image__isnull = False)

      # Weighted score: sales (50%) + ratings (30%) + views (20%)
      queryset = queryset.annotate(
          score=ExpressionWrapper(
              (F('discount') + F('total_sales') * 0.5) + (F('total_ratings') * 0.5) / F('total_review') + (F('views') * 0.2),
              output_field=FloatField()
          )
      ).order_by('-score')[:12]
      products = FurnitureProductSerializer(queryset, many=True)
      cache.set(cache_key, products.data, 300)
      return products.data
  
    except Exception as e:
      print(str(e))
      return []
