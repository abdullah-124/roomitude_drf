from rest_framework.serializers import ModelSerializer, SerializerMethodField
from products.models import FurnitureProduct
from order.models import Order,OrderItem



class OrderItemSerializer(ModelSerializer):
    total_price = SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_total_price(self, obj):
        return obj.get_total_price()
    
class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True, read_only = True)
    class Meta: 
        model = Order
        fields = "__all__"