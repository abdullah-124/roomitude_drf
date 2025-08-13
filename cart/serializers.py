from decimal import Decimal, ROUND_HALF_UP
from rest_framework import serializers
from products.models import FurnitureProduct
from cart.models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name', read_only=True)
    exact_price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'name', 'exact_price', 'image', 'quantity', 'total_price', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']
    # exact price
    def get_exact_price(self, obj):
        product = obj.product
        price = product.price  # DecimalField
        if hasattr(product, 'discount') and product.discount:
            discount_decimal = Decimal(product.discount) / Decimal(100)
            exact_price = price * (Decimal(1) - discount_decimal)
            # Round to 2 decimal places
            return exact_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)  
    def get_image(self, obj):
        if obj.product.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product.image.url)
            return obj.product.image.url
        return None
    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        quantity = validated_data.get('quantity', 1)
        
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            
        return cart_item

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)

    def create(self, validated_data):
        user = self.context['request'].user
        product = FurnitureProduct.objects.get(id=validated_data['product_id'])
        quantity = validated_data['quantity']
        
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            
        return cart_item