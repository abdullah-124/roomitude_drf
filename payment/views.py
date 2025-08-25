# Create your views here.
import stripe
from django.conf import settings
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from order.models import Order
from payment.models import Payment
from order.serializers import OrderSerializer

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class StripePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            order_id = data.get("order_id")

            order = Order.objects.get(id=order_id, user=request.user)
            amount = order.total
            if order.is_paid:  # or order.status == "paid"
                raise ValidationError("This order has already been paid.")
            intent = stripe.PaymentIntent.create(
                amount=Decimal(amount * 100).to_integral_value(),  # amount in cents
                currency="usd",
                metadata={"user_id": request.user.id, "order_id": order.id},
            )
            serializer = OrderSerializer(order)
            return Response({"order": serializer.data, "clientSecret": intent.client_secret})
        except Exception as e:
            return Response({"message": str(e)}, status=400)

# confirm the payment and update the order status
class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        payment_id = request.data.get("payment_id")

        # Double check with Stripe
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_id)
            metadata = payment_intent.get("metadata", {})
            order_id_stripe = metadata.get("order_id")
            user_id_stripe = metadata.get("user_id")
            if(order_id_stripe != str(order_id) or str(user_id_stripe) != str(request.user.id)):
                return Response({"error": "Order ID or User ID mismatch"}, status=400)
            if payment_intent.status == "succeeded":
                order = Order.objects.get(id=order_id, user=request.user)
                order.is_paid = True
                order.transaction_id = payment_id
                order.save()
                payment = Payment.objects.create(
                    order=order,
                    user = request.user,
                    transaction_id=payment_id,
                    amount=order.total,
                    status="completed",
                )
                payment.save()
                return Response({"status": "success"}, status=200)
        except Exception as e:
            return Response({"status": "failed", "message": str(e)}, status=400)
