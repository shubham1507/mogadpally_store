from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.cart.models import Cart
from apps.catalog.models import Product

from .models import Order, OrderItem


class CheckoutService:
    """
    Handles converting a user's cart into an order.
    """

    TAX_PERCENTAGE = Decimal("0.18")
    SHIPPING_CHARGE = Decimal("0.00")

    @classmethod
    @transaction.atomic
    def checkout(cls, user):
        try:
            cart = Cart.objects.prefetch_related(
                "items__product"
            ).get(user=user)

        except Cart.DoesNotExist:
            raise ValidationError("Cart not found.")

        cart_items = cart.items.all()

        if not cart_items.exists():
            raise ValidationError("Your cart is empty.")

        subtotal = Decimal("0.00")

        for item in cart_items:

            product = item.product

            if item.quantity > product.stock_quantity:
                raise ValidationError(
                    f"Only {product.stock_quantity} items available for '{product.name}'."
                )

            subtotal += item.total_price

        tax = (subtotal * cls.TAX_PERCENTAGE).quantize(
            Decimal("0.01")
        )

        shipping = cls.SHIPPING_CHARGE

        discount = Decimal("0.00")

        total = subtotal + tax + shipping - discount

        order = Order.objects.create(
            user=user,
            subtotal=subtotal,
            tax=tax,
            shipping_charge=shipping,
            discount=discount,
            total=total,
        )

        for item in cart_items:

            product = item.product

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_sku=product.sku,
                quantity=item.quantity,
                price=item.price_at_addition,
                total=item.total_price,
            )

            product.stock_quantity -= item.quantity
            product.save(update_fields=["stock_quantity"])

        cart.items.all().delete()

        return order