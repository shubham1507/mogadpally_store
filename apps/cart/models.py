import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.catalog.models import Product


class Cart(models.Model):
    """
    Each user has exactly one active shopping cart.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"{self.user.email}'s Cart"

    @property
    def total_items(self):
        """
        Total quantity of products in the cart.
        """
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """
        Sum of all cart item subtotals.
        """
        return sum(
            (item.subtotal for item in self.items.all()),
            Decimal("0.00"),
        )

    @property
    def shipping_charge(self):
        """
        Free shipping above ₹999.
        """
        return Decimal("0.00") if self.subtotal >= Decimal("999.00") else Decimal("50.00")

    @property
    def tax(self):
        """
        GST placeholder.
        Currently 0%.
        """
        return Decimal("0.00")

    @property
    def discount(self):
        """
        Coupon support will come later.
        """
        return Decimal("0.00")

    @property
    def grand_total(self):
        return (
            self.subtotal
            + self.shipping_charge
            + self.tax
            - self.discount
        )


class CartItem(models.Model):
    """
    A single product inside the user's cart.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField(default=1)

    price_snapshot = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_per_cart",
            )
        ]

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    @property
    def subtotal(self):
        return self.price_snapshot * self.quantity

    def save(self, *args, **kwargs):
        """
        Capture product price when first added.
        """
        if not self.price_snapshot:
            self.price_snapshot = self.product.price

        super().save(*args, **kwargs)