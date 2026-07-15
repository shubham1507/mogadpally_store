from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name_snapshot", "quantity", "unit_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "status", "shipping_address", "billing_address",
            "subtotal_amount", "discount_amount", "shipping_amount", "total_amount",
            "payment_status", "coupon_code", "items", "created_at",
        ]
        read_only_fields = [f for f in fields if f != "shipping_address"]


class CreateOrderSerializer(serializers.Serializer):
    shipping_address_id = serializers.UUIDField()
    billing_address_id = serializers.UUIDField(required=False)
    coupon_code = serializers.CharField(required=False, allow_blank=True)
