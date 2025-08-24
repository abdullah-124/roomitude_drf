from django.urls import path
from payment.views import StripePaymentIntentView

urlpatterns = [
    path("stripe/create-payment-intent/", StripePaymentIntentView.as_view(), name="create-payment-intent"),
]
