from django.urls import path
from .views import CreatePaymentIntentView, RazorpayWebhookView, PaymentStatusView

urlpatterns = [
    path("create-intent", CreatePaymentIntentView.as_view(), name="payment-create-intent"),
    path("webhook", RazorpayWebhookView.as_view(), name="payment-webhook"),
    path("<uuid:order_id>/status", PaymentStatusView.as_view(), name="payment-status"),
]
