from django.urls import path

from .views import (
    CartView,
    AddToCartView,
    CartItemView,
)

urlpatterns = [
    path(
        "cart",
        CartView.as_view(),
        name="cart",
    ),

    path(
        "cart/items",
        AddToCartView.as_view(),
        name="add-to-cart",
    ),

    path(
        "cart/items/<uuid:item_id>",
        CartItemView.as_view(),
        name="cart-item",
    ),
]