from django.urls import path

from .views import (
    CODPaymentAPIView,
    PaymentHistoryAPIView,
    RazorpayOrderAPIView,
    RazorpayVerifyAPIView,
)

app_name = "payments"

urlpatterns = [
    path(
        "cod/",
        CODPaymentAPIView.as_view(),
        name="cod-payment",
    ),
    path(
        "razorpay/",
        RazorpayOrderAPIView.as_view(),
        name="razorpay-order",
    ),
    path(
        "verify/",
        RazorpayVerifyAPIView.as_view(),
        name="verify-payment",
    ),
    path(
        "",
        PaymentHistoryAPIView.as_view(),
        name="payment-history",
    ),
]
