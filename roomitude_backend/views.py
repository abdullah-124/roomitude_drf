from django.http import HttpResponse
from category.models import Category
import json

data = [
  {
    "name": "Office Chair",
    "slug": "office-chair"
  },
  {
    "name": "Dining Chair",
    "slug": "dining-chair"
  },
  {
    "name": "Lounge Chair",
    "slug": "lounge-chair"
  },
  {
    "name": "Rocking Chair",
    "slug": "rocking-chair"
  },
  {
    "name": "Recliner Chair",
    "slug": "recliner-chair"
  },
  {
    "name": "Accent Chair",
    "slug": "accent-chair"
  },
  {
    "name": "Folding Chair",
    "slug": "folding-chair"
  },
  {
    "name": "Bean Bag Chair",
    "slug": "bean-bag-chair"
  },
  {
    "name": "Bar Stool",
    "slug": "bar-stool"
  },
  {
    "name": "Gaming Chair",
    "slug": "gaming-chair"
  }
]

def my_function(req):
    categories = Category.objects.all()
    
    data = [
        {
            "id": category.id,
            "name": category.name,
            "slug": category.slug
        }
        for category in categories
    ]

    return HttpResponse(json.dumps(data), content_type="application/json")