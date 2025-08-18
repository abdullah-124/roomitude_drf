from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from wishlist.serializers import WishlistSerializer
from wishlist.models import Wishlist

# Create your views here.
class WishList_View(ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)