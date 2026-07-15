import uuid
from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.models import Cart
from apps.users.models import Address
from .models import Order, OrderItem, Coupon
from .serializers import OrderSerializer, CreateOrderSerializer


def _generate_order_number():
    return f"MB-{timezone.now().year}-{uuid.uuid4().hex[:6].upper()}"


class CreateOrderView(APIView):
    """
    POST /api/v1/orders
    Creates an order from the user's current cart, decrements stock, and clears the cart.
    Wrapped in a transaction so a mid-way failure never leaves stock over-decremented
    or the order half-created.
    """
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        payload = CreateOrderSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        data = payload.validated_data

        cart = Cart.objects.select_related().prefetch_related("items__product").get(user=request.user)
        if not cart.items.exists():
            raise ValidationError("Cart is empty.")

        shipping_address = Address.objects.get(id=data["shipping_address_id"], user=request.user)
        billing_address_id = data.get("billing_address_id")
        billing_address = (
            Address.objects.get(id=billing_address_id, user=request.user) if billing_address_id else None
        )

        subtotal = Decimal("0.00")
        # lock product rows for update so concurrent checkouts can't both oversell the last unit
        items_snapshot = []
        for item in cart.items.select_related("product"):
            product = type(item.product).objects.select_for_update().get(id=item.product_id)
            if product.stock_quantity < item.quantity:
                raise ValidationError(f"Insufficient stock for {product.name}.")
            items_snapshot.append((product, item.quantity))
            subtotal += product.price * item.quantity

        discount = Decimal("0.00")
        coupon_code = data.get("coupon_code", "")
        if coupon_code:
            coupon = Coupon.objects.filter(code=coupon_code, is_active=True).first()
            if not coupon or not (coupon.valid_from <= timezone.now() <= coupon.valid_to):
                raise ValidationError("Invalid or expired coupon.")
            if subtotal < coupon.min_order_value:
                raise ValidationError(f"Minimum order value for this coupon is {coupon.min_order_value}.")
            discount = coupon.discount_value if coupon.discount_type == "flat" else subtotal * coupon.discount_value / 100
            coupon.times_used += 1
            coupon.save(update_fields=["times_used"])

        shipping_amount = Decimal("0.00")  # TODO: wire up real shipping calculation
        total = subtotal - discount + shipping_amount

        order = Order.objects.create(
            order_number=_generate_order_number(),
            user=request.user,
            shipping_address=shipping_address,
            billing_address=billing_address,
            subtotal_amount=subtotal,
            discount_amount=discount,
            shipping_amount=shipping_amount,
            total_amount=total,
            coupon_code=coupon_code,
        )
        for product, quantity in items_snapshot:
            OrderItem.objects.create(
                order=order, product=product, product_name_snapshot=product.name,
                quantity=quantity, unit_price=product.price,
            )
            product.stock_quantity -= quantity
            product.save(update_fields=["stock_quantity"])

        cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    """GET /api/v1/orders/list — current user's order history"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    """GET /api/v1/orders/:id"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CancelOrderView(APIView):
    """POST /api/v1/orders/:id/cancel — only allowed while pending/confirmed"""
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        order = Order.objects.select_for_update().get(id=pk, user=request.user)
        if order.status not in ("pending", "confirmed"):
            raise ValidationError("Order can no longer be cancelled.")
        order.status = "cancelled"
        order.save(update_fields=["status"])
        # restock
        for item in order.items.select_related("product"):
            item.product.stock_quantity += item.quantity
            item.product.save(update_fields=["stock_quantity"])
        return Response(OrderSerializer(order).data)
