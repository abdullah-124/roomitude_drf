from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import transaction
from decimal import Decimal
# views.py
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView 

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
            shipping_cost = Decimal(str(request.data.get("shipping_cost", 10)))
            discounted = sub_total * (Decimal(100) - discount) / Decimal(100)
            total = discounted + shipping_cost
            
            summery['sub_total'] = sub_total
            summery['total'] = total
            summery['items_count'] = len(result)
                
            return Response({
                'items': result, 'summery': summery
            })
        except Exception as e: 
            return Response({'message': str(e)})
        
# Place ORDER VIEW
class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        data = request.data['order']
        summary = data['summery']
        items = data['items']
        billing_info = data['billing_information']
        # return Response({'data': items})
        if not items:
            return Response({"error": "No items in order"}, status=status.HTTP_400_BAD_REQUEST)
        sub_total = sum(Decimal(str(item["exact_price"])) * item["quantity"] for item in items)
        if sub_total != Decimal(str(summary.get("sub_total"))):
            return Response({"error": "Invalid order summary"}, status=status.HTTP_400_BAD_REQUEST)
        discount=Decimal(summary.get("discount", 0))
        shipping_cost=Decimal(summary.get("shipping_cost", 10))
        total = sub_total - (sub_total * discount / 100) + shipping_cost
        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                user=user,
                full_name=billing_info.get('full_name') or user.get_full_name(),
                email=billing_info.get('email') or user.email,
                phone_number=billing_info.get('phone_number') or user.phone_number,
                address=billing_info.get('address') or user.address,
                city=billing_info.get('city') or '',
                postal_code=billing_info.get('postal_code') or '',
                shipping_method=summary.get("shipping"),
                sub_total=sub_total,
                discount=discount,
                shipping_cost=shipping_cost,
                total=total,
                )

                # Create order items
                for item in items:
                    product = FurnitureProduct.objects.get(id=item["product_id"])
                    if product.stock_quantity < item["quantity"]:
                        raise ValueError(f"{product.name} not available in requested quantity")

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name = product.name,
                        quantity=item["quantity"],
                        product_price=item["exact_price"],
                    )

                    # Update stock and seals
                    # product.stock_quantity -= item["quantity"]
                    # product.total_sales += items['quantity']
                    # product.save()
                cart_items = user.cart_items.all()
                cart_items.delete()
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    model = Order

    def get(self, request, pk=None):
        try:
            queryset = self.model.objects.filter(user=request.user)
            if(pk):
                order = get_object_or_404(queryset,id=pk)
                serializer = self.serializer_class(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            serializer = self.serializer_class(queryset, many=True)
            return Response({'orders': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)