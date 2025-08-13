from django.shortcuts import get_object_or_404
# rest framwork 
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# local 
from cart.serializers import CartItemSerializer, AddToCartSerializer
from cart.models import CartItem


# Create your views here.
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    # return cart items of requested user
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('product')
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    """Add item to cart - handles existing items"""
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        serializer = AddToCartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            cart_item = serializer.save()
            response_serializer = CartItemSerializer(cart_item)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['patch'])
    def update_quantity(self, request, pk=None):
        """Update item quantity"""
        cart_item = self.get_object()
        quantity = request.data.get('quantity')
        
        if quantity and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)
        
        return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def clear_cart(self, request):
        """Clear all items from cart"""
        deleted_count = self.get_queryset().delete()[0]
        return Response({
            'message': f'Removed {deleted_count} items from cart'
        }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def total(self, request):
        """Get cart total"""
        cart_items = self.get_queryset()
        total = sum(item.total_price for item in cart_items)
        return Response({
            'total': total,
            'item_count': cart_items.count()
        })