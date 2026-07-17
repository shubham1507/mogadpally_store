from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Payment details.
    """

    class Meta:
        model = Payment

        fields = (
            "id",
            "order",
            "provider",
            "status",
            "amount",
            "currency",
            "payment_id",
            "transaction_id",
            "gateway_order_id",
            "paid_at",
            "created_at",
        )

        read_only_fields = fields


class CODPaymentSerializer(serializers.Serializer):
    """
    Cash On Delivery request.
    """

    order_id = serializers.UUIDField()


class RazorpayPaymentSerializer(serializers.Serializer):
    """
    Razorpay payment request.
    """

    order_id = serializers.UUIDField()


class PaymentHistorySerializer(serializers.ModelSerializer):
    """
    User payment history.
    """

    class Meta:
        model = Payment

        fields = (
            "id",
            "provider",
            "status",
            "amount",
            "currency",
            "created_at",
        )

class RazorpayOrderSerializer(serializers.Serializer):

    order_id = serializers.UUIDField()

class RazorpayVerifySerializer(serializers.Serializer):
    razorpay_payment_id = serializers.CharField()
    razorpay_order_id = serializers.CharField()
    razorpay_signature = serializers.CharField()