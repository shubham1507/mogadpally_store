from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .models import Order, OrderStatus
from .serializers import (
    CheckoutResponseSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
)
from .services import CheckoutService


class CheckoutAPIView(APIView):
    """
    Convert authenticated user's cart into an order.
    """

    permission_classes = [IsAuthenticated]
    @extend_schema(request=None,responses={201: CheckoutResponseSerializer})
    def post(self, request):
        order = CheckoutService.checkout(request.user)

        serializer = CheckoutResponseSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class OrderListAPIView(generics.ListAPIView):
    """
    List logged-in user's orders.
    """

    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .order_by("-created_at")
        )


class OrderDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve single order.
    """

    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related("items")


class CancelOrderAPIView(APIView):
    """
    Cancel pending order.
    """

    permission_classes = [IsAuthenticated]
    @extend_schema(request=None,responses={201: CheckoutResponseSerializer})
    def post(self, request, id):

        try:
            order = Order.objects.get(
                id=id,
                user=request.user,
            )

        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if order.status != OrderStatus.PENDING:
            return Response(
                {
                    "detail": "Only pending orders can be cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = OrderStatus.CANCELLED
        order.save(update_fields=["status"])

        return Response(
            {
                "message": "Order cancelled successfully."
            }
        )