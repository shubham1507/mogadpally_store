from django.urls import path

from .views import (
    CancelOrderAPIView,
    CheckoutAPIView,
    OrderDetailAPIView,
    OrderListAPIView,
)

app_name = "orders"

urlpatterns = [
    path(
        "checkout/",
        CheckoutAPIView.as_view(),
        name="checkout",
    ),
    path(
        "",
        OrderListAPIView.as_view(),
        name="order-list",
    ),
    path(
        "<uuid:id>/",
        OrderDetailAPIView.as_view(),
        name="order-detail",
    ),
    path(
        "<uuid:id>/cancel/",
        CancelOrderAPIView.as_view(),
        name="cancel-order",
    ),
]