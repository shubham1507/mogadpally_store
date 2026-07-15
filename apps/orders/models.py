import uuid
from django.conf import settings
from django.db import models
from apps.catalog.models import Product
from apps.users.models import Address


class Coupon(models.Model):
    DISCOUNT_TYPES = [("flat", "Flat"), ("percent", "Percent")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    times_used = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"), ("confirmed", "Confirmed"), ("shipped", "Shipped"),
        ("delivered", "Delivered"), ("cancelled", "Cancelled"), ("refunded", "Refunded"),
    ]
    PAYMENT_STATUS_CHOICES = [
        ("unpaid", "Unpaid"), ("paid", "Paid"), ("failed", "Failed"), ("refunded", "Refunded"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="+")
    billing_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="+", null=True, blank=True)
    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="unpaid")
    coupon_code = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name_snapshot = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
