from decimal import Decimal

from django.conf import settings
from django.db import models




class DiscountType(models.TextChoices):
    PERCENTAGE = "PERCENTAGE", "Percentage"
    FLAT = "FLAT", "Flat"


class Coupon(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
        default=DiscountType.PERCENTAGE,
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    minimum_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    maximum_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    usage_limit = models.PositiveIntegerField(
        default=1,
    )

    used_count = models.PositiveIntegerField(
        default=0,
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.code
    
class UserCoupon(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
    )

    used_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "user",
            "coupon",
        )

    def __str__(self):
        return f"{self.user.email} - {self.coupon.code}"
    





   