from django.utils import timezone

from apps.orders.models import OrderStatus

from .gateway import RazorpayGateway
from .models import PaymentStatus


class RazorpayVerificationService:

    @staticmethod
    def verify(
        payment,
        payment_id,
        order_id,
        signature,
    ):

        client = RazorpayGateway.client()

        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
        )

        payment.payment_id = payment_id
        payment.transaction_id = payment_id
        payment.signature = signature

        payment.status = PaymentStatus.SUCCESS
        payment.paid_at = timezone.now()

        payment.save()

        payment.order.status = OrderStatus.CONFIRMED
        payment.order.save()

        return payment