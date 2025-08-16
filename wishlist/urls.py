from django.urls import path
from wishlist.views import WishList_View

urlpatterns = [
    path('', WishList_View.as_view() )
]
