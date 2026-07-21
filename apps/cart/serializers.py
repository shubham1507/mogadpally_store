from rest_framework import serializers

from apps.catalog.serializers import ProductListSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for a single cart item.
    """

    product = ProductListSerializer(read_only=True)

    total_price = serializers.SerializerMethodField()
    def get_total_price(self, obj) -> str:
        return obj.total_price

    
    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "price_at_addition",
            "total_price",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "price_at_addition",
            "total_price",
            "created_at",
        ]


class CartSerializer(serializers.ModelSerializer):
    """
    Complete cart response.
    """

    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    total_items = serializers.IntegerField(
        read_only=True,
    )

    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_items",
            "subtotal",
            "updated_at",
        ]
        read_only_fields = fields


class AddToCartSerializer(serializers.Serializer):
    """
    Request body for Add to Cart API.
    """

    product_id = serializers.UUIDField()

    quantity = serializers.IntegerField(
        min_value=1,
        default=1,
    )


class UpdateCartItemSerializer(serializers.Serializer):
    """
    Request body for Update Quantity API.
    """

    quantity = serializers.IntegerField(
        min_value=1,
    )