from django.urls import path
from .views import CartView, CartItemView

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("items", CartItemView.as_view(), name="cart-item-create"),
    path("items/<uuid:product_id>", CartItemView.as_view(), name="cart-item-detail"),
]

# NOTE: wishlist lives in apps/cart/wishlist_urls.py and is mounted separately
# in config/urls.py at /api/v1/wishlist, even though the model is in this app —
# it's the same domain (user's saved products) so it didn't warrant its own app.
