from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from wishlist.serializers import WishlistSerializer
from wishlist.models import Wishlist
from products.models import FurnitureProduct

# Create your views here.
class WishList_View(ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get all wishlist items for logged-in user"""
        wishlist_items = self.queryset.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Add a product to wishlist"""
        try:
            product_id = request.data.get("product_id")
            if not product_id:
                return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            # check if already in wishlist
            product = get_object_or_404(FurnitureProduct,id=product_id)
            wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
            serializer = WishlistSerializer(wishlist_item, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    # PK WILL recieve as a product_id not wishlist id 
    def destroy(self, request, pk=None):
        try:
            product = get_object_or_404(FurnitureProduct, id=pk)
            wishlist_item = get_object_or_404(Wishlist, product=product, user=request.user)
            wishlist_item.delete()
        except Exception as e: 
            Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": f"{product.name} removed"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        """Clear all wishlist items for logged-in user"""
        Wishlist.objects.filter(user=request.user).delete()
        return Response({"message": "Wishlist cleared"}, status=status.HTTP_200_OK)