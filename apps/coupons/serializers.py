from rest_framework import serializers


class ApplyCouponSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    code = serializers.CharField(max_length=50)