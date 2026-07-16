from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "total_items",
        "subtotal",
        "updated_at",
    )

    search_fields = (
        "user__email",
    )

    inlines = [
        CartItemInline,
    ]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "product",
        "quantity",
        "price_at_addition",
        "total_price",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "product__name",
        "cart__user__email",
    )