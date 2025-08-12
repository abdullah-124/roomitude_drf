from django.http import HttpResponse, JsonResponse
from category.models import Category
from products.models import FurnitureProduct
from roomitude_backend.data import products
import json
import random


def my_function(req):
  if(req.user.is_authenticated and req.user.username == 'admin'):
    f = FurnitureProduct.objects.values()
    data = list(f)
    return JsonResponse(data, safe=False)

  return HttpResponse('you do not have the permission to run this page 404 unauthorized')