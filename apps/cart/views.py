from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
)
from .services import (
    get_or_create_cart,
    add_to_cart,
    update_cart_item,
    remove_cart_item,
    clear_cart,
)


class CartView(APIView):
    """
    GET    /api/v1/cart
    DELETE /api/v1/cart
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart).data)

    def delete(self, request):
        cart = clear_cart(request.user)
        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK,
        )


class AddToCartView(APIView):
    """
    POST /api/v1/cart/items
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cart = add_to_cart(
                user=request.user,
                product_id=serializer.validated_data["product_id"],
                quantity=serializer.validated_data["quantity"],
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK,
        )


class CartItemView(APIView):
    """
    PATCH  /api/v1/cart/items/<uuid:item_id>
    DELETE /api/v1/cart/items/<uuid:item_id>
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cart = update_cart_item(
                user=request.user,
                cart_item_id=item_id,
                quantity=serializer.validated_data["quantity"],
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(CartSerializer(cart).data)

    def delete(self, request, item_id):
        cart = remove_cart_item(
            user=request.user,
            cart_item_id=item_id,
        )

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK,
        )