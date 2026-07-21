from rest_framework import serializers

from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = (
            "id",
            "code",
            "description",
            "discount_type",
            "discount_value",
        )


class ApplyCouponSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    code = serializers.CharField(max_length=50)