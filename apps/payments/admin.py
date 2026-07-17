from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "user",
        "provider",
        "status",
        "amount",
        "currency",
        "payment_id",
        "created_at",
    )

    list_filter = (
        "provider",
        "status",
        "created_at",
    )

    search_fields = (
        "payment_id",
        "transaction_id",
        "gateway_order_id",
        "order__id",
        "user__email",
    )

    readonly_fields = (
        "gateway_response",
        "created_at",
        "updated_at",
        "paid_at",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Payment Information",
            {
                "fields": (
                    "order",
                    "user",
                    "provider",
                    "status",
                    "amount",
                    "currency",
                )
            },
        ),
        (
            "Gateway Information",
            {
                "fields": (
                    "payment_id",
                    "transaction_id",
                    "gateway_order_id",
                    "signature",
                    "gateway_response",
                )
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "paid_at",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )