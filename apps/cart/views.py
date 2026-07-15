from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.catalog.models import Product
from apps.catalog.serializers import ProductListSerializer
from .models import Cart, CartItem, WishlistItem
from .serializers import CartSerializer


class CartView(APIView):
    """GET /api/v1/cart, DELETE /api/v1/cart (clear)"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)

    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemView(APIView):
    """
    POST   /api/v1/cart/items          { product_id, quantity } — add or set quantity
    PATCH  /api/v1/cart/items/:id      { quantity }
    DELETE /api/v1/cart/items/:id
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=request.data["product_id"], is_active=True)
        quantity = int(request.data.get("quantity", 1))
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
        if not created:
            item.quantity = quantity
            item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    def patch(self, request, product_id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item = CartItem.objects.get(cart=cart, product_id=product_id)
        item.quantity = int(request.data["quantity"])
        item.save()
        return Response(CartSerializer(cart).data)

    def delete(self, request, product_id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response(CartSerializer(cart).data)


class WishlistView(APIView):
    """
    GET    /api/v1/wishlist
    POST   /api/v1/wishlist/:product_id
    DELETE /api/v1/wishlist/:product_id
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(wishlistitem__user=request.user)
        return Response(ProductListSerializer(products, many=True).data)

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id, is_active=True)
        WishlistItem.objects.get_or_create(user=request.user, product=product)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        WishlistItem.objects.filter(user=request.user, product_id=product_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
