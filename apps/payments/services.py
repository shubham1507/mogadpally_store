from django.db import transaction
from django.utils import timezone

from apps.orders.models import Order, OrderStatus

from .exceptions import PaymentAlreadyExists
from .gateway import RazorpayGateway
from .models import (
    Payment,
    PaymentProvider,
    PaymentStatus,
)
from .utils import amount_to_paise


class PaymentService:
    """
    Base Payment Service
    """

    @staticmethod
    @transaction.atomic
    def create_payment(
        *,
        order: Order,
        provider: str,
    ) -> Payment:

        if Payment.objects.filter(order=order).exists():
            raise PaymentAlreadyExists(
                "Payment already exists for this order."
            )

        payment = Payment.objects.create(
            order=order,
            user=order.user,
            provider=provider,
            amount=order.total,
            currency="INR",
            status=PaymentStatus.PENDING,
        )

        return payment


class CODPaymentService:
    """
    Cash On Delivery Payment
    """

    @staticmethod
    @transaction.atomic
    def create(order: Order) -> Payment:

        payment = PaymentService.create_payment(
            order=order,
            provider=PaymentProvider.COD,
        )

        payment.status = PaymentStatus.SUCCESS
        payment.paid_at = timezone.now()

        payment.save(
            update_fields=[
                "status",
                "paid_at",
            ]
        )

        order.status = OrderStatus.CONFIRMED

        order.save(
            update_fields=[
                "status",
            ]
        )

        return payment


class RazorpayPaymentService:
    """
    Razorpay Order Creation Service
    """

    @staticmethod
    @transaction.atomic
    def create(order: Order) -> Payment:

        payment = PaymentService.create_payment(
            order=order,
            provider=PaymentProvider.RAZORPAY,
        )

        client = RazorpayGateway.client()

        razorpay_order = client.order.create(
            {
                "amount": amount_to_paise(order.total),
                "currency": "INR",
                "payment_capture": 1,
                "receipt": str(order.id),
            }
        )

        payment.gateway_order_id = razorpay_order["id"]
        payment.gateway_response = razorpay_order

        payment.save(
            update_fields=[
                "gateway_order_id",
                "gateway_response",
            ]
        )

        return payment