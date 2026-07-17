from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False

    readonly_fields = (
        "product",
        "product_name",
        "product_sku",
        "quantity",
        "price",
        "total",
    )

    fields = (
        "product",
        "product_name",
        "product_sku",
        "quantity",
        "price",
        "total",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "status",
        "total_items",
        "subtotal",
        "discount",
        "tax",
        "shipping_charge",
        "total",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "id",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "subtotal",
        "discount",
        "tax",
        "shipping_charge",
        "total",
    )

    ordering = (
        "-created_at",
    )

    inlines = [
        OrderItemInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product_name",
        "quantity",
        "price",
        "total",
    )

    search_fields = (
        "order__id",
        "product_name",
        "product_sku",
    )

    readonly_fields = (
        "total",
    )

    ordering = (
        "-id",
    )