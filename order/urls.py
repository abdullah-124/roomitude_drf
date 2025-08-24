from django.urls import path
from order.views import CheckoutView, PlaceOrderView, OrderView
urlpatterns = [
    path('', OrderView.as_view()),
    path('<int:pk>/', OrderView.as_view()),
    path('checkout/', CheckoutView.as_view()),
    path('place_order/', PlaceOrderView.as_view()),
]
