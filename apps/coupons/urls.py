from django.urls import path

from .views import (
    ApplyCouponAPIView,
    CouponListAPIView,
)

app_name = "coupons"

urlpatterns = [
    path(
        "",
        CouponListAPIView.as_view(),
        name="coupon-list",
    ),

    path(
        "apply/",
        ApplyCouponAPIView.as_view(),
        name="apply-coupon",
    ),
]