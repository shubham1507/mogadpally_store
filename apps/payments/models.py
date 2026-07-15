import uuid
from django.db import models
from apps.orders.models import Order


class Payment(models.Model):
    STATUS_CHOICES = [
        ("initiated", "Initiated"), ("success", "Success"),
        ("failed", "Failed"), ("refunded", "Refunded"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    gateway = models.CharField(max_length=30, default="razorpay")
    gateway_order_id = models.CharField(max_length=150, blank=True)
    gateway_payment_id = models.CharField(max_length=150, blank=True, unique=True, null=True)
    method = models.CharField(max_length=30, blank=True)  # upi | card | netbanking | wallet
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="initiated")
    created_at = models.DateTimeField(auto_now_add=True)
