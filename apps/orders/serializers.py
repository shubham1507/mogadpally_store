from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "product_name",
            "product_sku",
            "quantity",
            "price",
            "total",
        )
        read_only_fields = fields


class OrderListSerializer(serializers.ModelSerializer):
    total_items = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "subtotal",
            "tax",
            "shipping_charge",
            "discount",
            "total",
            "total_items",
            "created_at",
        )
        read_only_fields = fields


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    total_items = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "subtotal",
            "tax",
            "shipping_charge",
            "discount",
            "total",
            "total_items",
            "notes",
            "created_at",
            "updated_at",
            "items",
        )
        read_only_fields = fields


class CheckoutResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "total",
            "created_at",
        )
        read_only_fields = fields