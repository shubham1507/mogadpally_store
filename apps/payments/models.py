import uuid

from django.conf import settings
from django.db import models

from apps.orders.models import Order


class PaymentProvider(models.TextChoices):
    COD = "COD", "Cash On Delivery"
    RAZORPAY = "RAZORPAY", "Razorpay"
    STRIPE = "STRIPE", "Stripe"


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"
    CANCELLED = "CANCELLED", "Cancelled"
    REFUNDED = "REFUNDED", "Refunded"


class Payment(models.Model):
    """
    Payment information for an order.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    provider = models.CharField(
        max_length=20,
        choices=PaymentProvider.choices,
        default=PaymentProvider.COD,
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=10,
        default="INR",
    )

    payment_id = models.CharField(
        max_length=255,
        blank=True,
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
    )

    gateway_order_id = models.CharField(
        max_length=255,
        blank=True,
    )

    signature = models.TextField(
        blank=True,
    )

    gateway_response = models.JSONField(
        blank=True,
        null=True,
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"{self.order.id} - {self.provider} - {self.status}"