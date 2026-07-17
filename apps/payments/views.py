from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.models import Order

from apps.payments.serializers import RazorpayOrderSerializer
from apps.payments.services import RazorpayPaymentService

from .models import Payment
from .serializers import (
    CODPaymentSerializer,
    PaymentHistorySerializer,
    PaymentSerializer,
)
from .services import CODPaymentService


class CODPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

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