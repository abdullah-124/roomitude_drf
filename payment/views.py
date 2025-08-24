# Create your views here.
import stripe
from django.conf import settings
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from order.models import Order

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class StripePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            order_id = data.get("order_id")

            order = Order.objects.get(id=order_id, user=request.user)
            amount = order.total

            intent = stripe.PaymentIntent.create(
                amount=Decimal(amount * 100).to_integral_value(),  # amount in cents
                currency="usd",
                metadata={"user_id": request.user.id},
            )

            return Response({"clientSecret": intent.client_secret})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

# confirm the payment and update the order status
class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        payment_id = request.data.get("payment_id")

        # Double check with Stripe
        payment_intent = stripe.PaymentIntent.retrieve(payment_id)

        if payment_intent.status == "succeeded":
            order = Order.objects.get(id=order_id, user=request.user)
            order.payment_status = "paid"
            order.stripe_payment_id = payment_id
            order.save()
            return Response({"status": "success"})
        return Response({"status": "failed"}, status=400)
