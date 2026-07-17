from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from .exceptions import PaymentAlreadyExists

from apps.orders.models import Order, OrderStatus

from .models import (
    Payment,
    PaymentProvider,
    PaymentStatus,
)


class PaymentService:
    """
    Base payment service.
    """

    @staticmethod
    @transaction.atomic
    def create_payment(
        *,
        order: Order,
        provider: str,
    ) -> Payment:

        if hasattr(order, "payment"):
            raise PaymentAlreadyExists(
    "Payment already exists."
)

        return Payment.objects.create(
            order=order,
            user=order.user,
            provider=provider,
            amount=order.total,
            currency="INR",
            status=PaymentStatus.PENDING,
        )


class CODPaymentService:
    """
    Cash On Delivery payment.
    """

    @staticmethod
    @transaction.atomic
    def create(order: Order) -> Payment:

        payment = PaymentService.create_payment(
            order=order,
            provider=PaymentProvider.COD,
        )

        order.status = OrderStatus.CONFIRMED
        order.save(update_fields=["status"])

        payment.status = PaymentStatus.SUCCESS
        payment.paid_at = timezone.now()
        payment.save(
            update_fields=[
                "status",
                "paid_at",
            ]
        )

        return payment


class RazorpayPaymentService:
    """
    Placeholder for Razorpay integration.
    """

    @staticmethod
    @transaction.atomic
    def create(order: Order) -> Payment:

        payment = PaymentService.create_payment(
            order=order,
            provider=PaymentProvider.RAZORPAY,
        )

        # Razorpay Order Creation
        # Coming in next story.

        return payment