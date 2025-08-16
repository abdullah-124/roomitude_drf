from rest_framework.generics import ListAPIView
from wishlist.serializers import WishlistSerializer
from wishlist.models import Wishlist

# Create your views here.
class WishList_View(ListAPIView):
    serializer_class = WishlistSerializer
    def get_queryset(self):
        return Wishlist.objects.filter(user = self.request.user)