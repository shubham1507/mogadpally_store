from django.contrib import admin

from .models import Coupon, UserCoupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_type",
        "discount_value",
        "minimum_order_amount",
        "maximum_discount",
        "usage_limit",
        "used_count",
        "is_active",
        "start_date",
        "end_date",
    )

    list_filter = (
        "discount_type",
        "is_active",
    )

    search_fields = (
        "code",
    )

    ordering = (
        "-created_at",
    )


@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "coupon",
        "used_at",
    )

    search_fields = (
        "user__email",
        "coupon__code",
    )

    ordering = (
        "-used_at",
    )