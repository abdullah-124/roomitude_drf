from django.urls import path
from payment.views import StripePaymentIntentView, ConfirmPaymentView

urlpatterns = [
    path("stripe/create-payment-intent/", StripePaymentIntentView.as_view(), name="create-payment-intent"),
    path("stripe/confirm-payment/", ConfirmPaymentView.as_view(), name="confirm-payment"),
]
