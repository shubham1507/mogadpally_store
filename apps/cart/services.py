from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.catalog.models import Product

from .models import Cart, CartItem


def get_or_create_cart(user):
    """
    Returns the user's active cart.
    Creates one if it doesn't exist.
    """
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@transaction.atomic
def add_to_cart(user, product_id, quantity):
    """
    Add a product to the cart.

    If the product already exists in the cart,
    increase the quantity instead of creating
    another CartItem.
    """

    cart = get_or_create_cart(user)

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
    )

    if not product.in_stock:
        raise ValueError("Product is out of stock.")

    if quantity > product.stock_quantity:
        raise ValueError(
            "Requested quantity exceeds available stock."
        )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            "quantity": quantity,
            "price_at_addition": product.price,
        },
    )

    if not created:
        new_quantity = cart_item.quantity + quantity

        if new_quantity > product.stock_quantity:
            raise ValueError(
                "Requested quantity exceeds available stock."
            )

        cart_item.quantity = new_quantity
        cart_item.save(update_fields=["quantity", "updated_at"])

    return cart


@transaction.atomic
def update_cart_item(user, cart_item_id, quantity):
    """
    Update quantity of a cart item.
    """

    cart = get_or_create_cart(user)

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart=cart,
    )

    if quantity > cart_item.product.stock_quantity:
        raise ValueError(
            "Requested quantity exceeds available stock."
        )

    cart_item.quantity = quantity
    cart_item.save(update_fields=["quantity", "updated_at"])

    return cart


@transaction.atomic
def remove_cart_item(user, cart_item_id):
    """
    Remove one item from the cart.
    """

    cart = get_or_create_cart(user)

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart=cart,
    )

    cart_item.delete()

    return cart


@transaction.atomic
def clear_cart(user):
    """
    Remove every item from the user's cart.
    """

    cart = get_or_create_cart(user)

    cart.items.all().delete()

    return cart