from django.contrib import admin
from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name_snapshot", "quantity", "unit_price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "status", "payment_status", "total_amount", "created_at")
    list_filter = ("status", "payment_status", "created_at")
    search_fields = ("order_number", "user__email")
    inlines = [OrderItemInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_type", "discount_value", "is_active", "valid_from", "valid_to")
