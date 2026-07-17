from django.urls import path

from .views import (
    CODPaymentAPIView,
    PaymentHistoryAPIView,
)

app_name = "payments"

urlpatterns = [
    path(
        "cod/",
        CODPaymentAPIView.as_view(),
        name="cod-payment",
    ),
    path(
        "",
        PaymentHistoryAPIView.as_view(),
        name="payment-history",
    ),
]