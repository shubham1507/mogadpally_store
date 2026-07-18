from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.orders.models import Order

from .models import Coupon, DiscountType, UserCoupon


class CouponValidationError(Exception):
    pass


class CouponService:

    @staticmethod
    def validate_coupon(
        *,
        coupon: Coupon,
        order: Order,
        user,
    ):

        now = timezone.now()

        if not coupon.is_active:
            raise CouponValidationError(
                "Coupon is inactive."
            )

        if coupon.start_date > now:
            raise CouponValidationError(
                "Coupon is not active yet."
            )

        if coupon.end_date < now:
            raise CouponValidationError(
                "Coupon has expired."
            )

        if order.total < coupon.minimum_order_amount:
            raise CouponValidationError(
                "Minimum order amount not reached."
            )

        if coupon.used_count >= coupon.usage_limit:
            raise CouponValidationError(
                "Coupon usage limit exceeded."
            )

        if UserCoupon.objects.filter(
            user=user,
            coupon=coupon,
        ).exists():

            raise CouponValidationError(
                "Coupon already used."
            )

        return coupon

    @staticmethod
    def calculate_discount(
        *,
        coupon: Coupon,
        amount: Decimal,
    ) -> Decimal:

        if coupon.discount_type == DiscountType.FLAT:
            discount = coupon.discount_value

        else:
            discount = (
                amount * coupon.discount_value
            ) / Decimal("100")

        if (
            coupon.maximum_discount > 0
            and discount > coupon.maximum_discount
        ):
            discount = coupon.maximum_discount

        return discount.quantize(
            Decimal("0.01")
        )

    @staticmethod
    @transaction.atomic
    def apply_coupon(
        *,
        coupon: Coupon,
        order: Order,
        user,
    ):

        CouponService.validate_coupon(
            coupon=coupon,
            order=order,
            user=user,
        )

        discount = CouponService.calculate_discount(
            coupon=coupon,
            amount=order.total,
        )

        final_total = order.total - discount

        return {
            "coupon": coupon,
            "discount": discount,
            "final_total": final_total,
        }