import razorpay
from django.conf import settings
from django.db import transaction
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.models import Order
from .models import Payment

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class CreatePaymentIntentView(APIView):
    """POST /api/v1/payments/create-intent  { order_id } — creates a Razorpay order, returns key + order id for checkout.js"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order = Order.objects.get(id=request.data["order_id"], user=request.user)
        amount_paise = int(order.total_amount * 100)
        rp_order = razorpay_client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "receipt": order.order_number,
        })
        Payment.objects.create(
            order=order, gateway="razorpay", gateway_order_id=rp_order["id"], amount=order.total_amount,
        )
        return Response({
            "key_id": settings.RAZORPAY_KEY_ID,
            "razorpay_order_id": rp_order["id"],
            "amount": amount_paise,
            "currency": "INR",
        }, status=status.HTTP_201_CREATED)


class RazorpayWebhookView(APIView):
    """
    POST /api/v1/payments/webhook — called by Razorpay, not the browser.
    Verifies signature, then idempotently updates payment + order status.
    Keyed off gateway_payment_id uniqueness so retried webhooks don't double-process.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @transaction.atomic
    def post(self, request):
        signature = request.headers.get("X-Razorpay-Signature", "")
        try:
            razorpay_client.utility.verify_webhook_signature(
                request.body.decode(), signature, settings.RAZORPAY_KEY_SECRET,
            )
        except razorpay.errors.SignatureVerificationError:
            return Response({"error": "invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        payload = request.data
        event = payload.get("event")
        rp_payment = payload.get("payload", {}).get("payment", {}).get("entity", {})
        rp_payment_id = rp_payment.get("id")
        rp_order_id = rp_payment.get("order_id")

        payment = Payment.objects.filter(gateway_order_id=rp_order_id).first()
        if not payment or payment.gateway_payment_id == rp_payment_id:
            # already processed, or unknown order — ack anyway so Razorpay stops retrying
            return Response(status=status.HTTP_200_OK)

        payment.gateway_payment_id = rp_payment_id
        payment.method = rp_payment.get("method", "")
        if event == "payment.captured":
            payment.status = "success"
            payment.order.payment_status = "paid"
            payment.order.status = "confirmed"
        elif event == "payment.failed":
            payment.status = "failed"
            payment.order.payment_status = "failed"
        payment.save()
        payment.order.save(update_fields=["payment_status", "status"])
        return Response(status=status.HTTP_200_OK)


class PaymentStatusView(APIView):
    """GET /api/v1/payments/:order_id/status — for the client to poll after redirect"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)
        return Response({"payment_status": order.payment_status, "order_status": order.status})
