from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wishlist.views import WishList_View

router = DefaultRouter()
router.register('', WishList_View, basename='wishlist')

urlpatterns = [
    path('', include(router.urls) )
]
