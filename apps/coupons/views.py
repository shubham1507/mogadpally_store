from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from apps.orders.models import Order

from .models import Coupon
from .serializers import ApplyCouponSerializer
from .services import CouponService
from .serializers import (
    ApplyCouponSerializer,
    CouponSerializer,
)


class CouponListAPIView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CouponSerializer

    queryset = Coupon.objects.filter(
        is_active=True
    ).order_by("code")
    @extend_schema(
    summary="List Coupons",
    description="Returns all active coupons."
    )
    def list(self, request, *args, **kwargs):

        coupons = self.get_queryset()

        data = [
            {
                "id": coupon.id,
                "code": coupon.code,
                "description": coupon.description,
                "discount_type": coupon.discount_type,
                "discount_value": coupon.discount_value,
            }
            for coupon in coupons
        ]

        return Response(data)


class ApplyCouponAPIView(APIView):

    permission_classes = [IsAuthenticated]
    @extend_schema(
    request=ApplyCouponSerializer,
    responses={200: None},
    summary="Apply Coupon",
    description="Apply coupon on an order."
    )
    def post(self, request):

        serializer = ApplyCouponSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        coupon = get_object_or_404(
            Coupon,
            code=serializer.validated_data["code"],
        )

        order = get_object_or_404(
            Order,
            id=serializer.validated_data["order_id"],
            user=request.user,
        )

        result = CouponService.apply_coupon(
            coupon=coupon,
            order=order,
            user=request.user,
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )