from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from apps.orders.models import Order

from apps.payments.serializers import RazorpayOrderSerializer
from apps.payments.services import RazorpayPaymentService

from .models import Payment
from .serializers import (
    CODPaymentSerializer,
    PaymentHistorySerializer,
    PaymentSerializer,
    RazorpayVerifySerializer,
)
from .services import CODPaymentService


class CODPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
    request=CODPaymentSerializer,
    responses={201: PaymentSerializer},
    summary="Cash On Delivery Payment",
    description="Create COD payment for an order."
    )
    def post(self, request):

        serializer = CODPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = get_object_or_404(
            Order,
            id=serializer.validated_data["order_id"],
            user=request.user,
        )

        payment = CODPaymentService.create(order)

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED,
        )


class PaymentHistoryAPIView(ListAPIView):

    serializer_class = PaymentHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            user=self.request.user
        ).order_by("-created_at")
    
class RazorpayOrderAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]
    @extend_schema(
    request=RazorpayOrderSerializer,
    responses={201: PaymentSerializer},
    summary="Create Razorpay Order",
    description="Creates a Razorpay order for payment."
    )   
    def post(self, request):

        serializer = RazorpayOrderSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        order = get_object_or_404(
            Order,
            id=serializer.validated_data["order_id"],
            user=request.user,
        )

        payment = RazorpayPaymentService.create(
            order
        )

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED,
        )
    
class RazorpayVerifyAPIView(APIView):
    """
    Verify Razorpay payment signature and mark payment as successful.
    """

    permission_classes = [IsAuthenticated]
    @extend_schema(
    request=RazorpayVerifySerializer,
    responses={200: None},
    summary="Verify Razorpay Payment",
    description="Verify Razorpay payment signature."
    )
    def post(self, request):

        serializer = RazorpayVerifySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        payment = get_object_or_404(
            Payment,
            gateway_order_id=serializer.validated_data[
                "razorpay_order_id"
            ],
            user=request.user,
        )

        payment = RazorpayPaymentService.verify(
            payment=payment,
            razorpay_payment_id=serializer.validated_data[
                "razorpay_payment_id"
            ],
            razorpay_signature=serializer.validated_data[
                "razorpay_signature"
            ],
        )

        return Response(
            {
                "message": "Payment verified successfully",
                "payment_id": str(payment.id),
                "order_id": str(payment.order.id),
                "status": payment.status,
            },
            status=status.HTTP_200_OK,
        )