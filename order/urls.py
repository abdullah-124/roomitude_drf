from django.urls import path
from order.views import CheckoutView, PlaceOrderView
urlpatterns = [
    path('checkout/', CheckoutView.as_view()),
    path('place_order/', PlaceOrderView.as_view()),
]
