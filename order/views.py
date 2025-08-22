from django.conf import settings
from django.db import transaction
from decimal import Decimal
# views.py
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView 
from rest_framework.mixins import ListModelMixin, CreateModelMixin 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from cart.models import CartItem
from order.models import Order, OrderItem
from products.models import FurnitureProduct
from order.serializers import OrderItemSerializer, OrderSerializer


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try: 
            user = request.user
            cart_items = user.cart_items.all()
            data = request.data
            print("Incoming data:", data)
            summery = dict(data)  
            result = []
            sub_total = 0
            for item in cart_items: 
                product = item.product
                image_url = request.build_absolute_uri(product.image.url) if product.image else None
                rq_quantity = item.quantity
                available_quantity = product.stock_quantity
                quantity = min(rq_quantity,available_quantity)
                total = product.get_price() * quantity
                sub_total += total
                new_items = {
                    'id': item.id,
                    'product_id': product.id,
                    'name': product.name ,
                    'image': image_url,
                    'quantity': quantity,
                    'exact_price': product.get_price(),
                    'total_price': total   
                }
                if(available_quantity < rq_quantity):
                    new_items['message'] = f"You have requested for {rq_quantity} items but only {available_quantity} items are available"
                result.append(new_items)
                
            discount = Decimal(str(request.data.get("discount", 0)))
            shipping_price = Decimal(str(request.data.get("shipping", {}).get("price", 10)))
            discounted = sub_total * (Decimal(100) - discount) / Decimal(100)
            total = discounted + shipping_price
            
            summery['sub_total'] = sub_total
            summery['total'] = total
            summery['items_count'] = len(result)
                
            return Response({
                'items': result, 'summery': summery
            })
        except Exception as e: 
            return Response({'message': str(e)})
        
# ORDER VIEW
class PlaceOrderView(GenericAPIView, CreateModelMixin,ListModelMixin):
    serializer_class = OrderSerializer
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    def get(self, request):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response({'items':serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data['order']
        summary = data['summery']
        items = data['items']
        # return Response({'data': items})
        if not items:
            return Response({"error": "No items in order"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    sub_total=summary.get("sub_total"),
                    discount=summary.get("discount", 0),
                    shipping_method=summary["shipping"]["id"],
                    shipping_cost=summary["shipping"]["price"],
                    payment_method=summary["payment_method"],
                    total=summary.get("total"),
                )

                # Create order items
                for item in items:
                    product = FurnitureProduct.objects.get(id=item["product_id"])
                    if product.stock_quantity < item["quantity"]:
                        raise ValueError(f"{product.name} not available in requested quantity")

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item["quantity"],
                        product_price=item["exact_price"],
                    )

                    # Update stock and seals
                    # product.stock_quantity -= item["quantity"]
                    # product.total_sales += items['quantity']
                    # product.save()

                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)