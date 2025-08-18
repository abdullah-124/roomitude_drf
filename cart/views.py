from django.shortcuts import get_object_or_404
# rest framwork 
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# local 
from products.models import FurnitureProduct
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

    # Add item to cart - handles existing items 
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        serializer = AddToCartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            cart_item = serializer.save()
            response_serializer = CartItemSerializer(cart_item, context = {'request': request})
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
    # remove item form cart 
    @action(detail=True, methods=['delete'])
    def remove_cart_item(self, request, pk=None):
        try:
            cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
            cart_item.delete()
            return Response(
                {"message": f"Cart item {cart_item.product.name} deleted successfully"},
                status=status.HTTP_200_OK
            )
        except Exception as e: 
            return Response({'error': str(e)})



    @action(detail=False, methods=['delete'])
    def clear_cart(self, request):
        """Clear all items from cart"""
        deleted_count = self.get_queryset().delete()[0]
        return Response({
            'message': f'Removed {deleted_count} items from cart'
        }, status=status.HTTP_204_NO_CONTENT)
    @action(detail=False, methods=['post'], url_path='merge')
    def merge_cart(self, request):
        print('inside merge api endpoint')
        user = request.user
        items = request.data.get("items", [])

        if not user.is_authenticated:
            return Response({"error": "Authentication required"},status=status.HTTP_401_UNAUTHORIZED)

        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            if not product_id:
                continue  # skip invalid items
            try:
                product = FurnitureProduct.objects.get(id=product_id)
            except FurnitureProduct.DoesNotExist:
                continue  # skip items that don't exist

            # Get or create cart item
            cart_item, created = CartItem.objects.get_or_create(
                user=user,
                product=product,
                defaults={"quantity": quantity}
            )

            # If it already exists, update quantity
            if not created:
                cart_item.quantity = max(cart_item.quantity, quantity)
                cart_item.save()
            cart_Model = CartItem.objects.filter(user=user)
            results = CartItemSerializer(cart_Model, many=True, context={'request': self.request})
        return Response(
            {
                "message": "Cart merged successfully",
                "items": results.data
            },
            status=status.HTTP_200_OK
        )
    @action(detail=False, methods=['get'])
    def total(self, request):
        """Get cart total"""
        cart_items = self.get_queryset()
        total = sum(item.total_price for item in cart_items)
        return Response({
            'total': total,
            'item_count': cart_items.count()
        })