from django.db.models import Avg, Count
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ReviewSerializer,
)


# --------------------------------------------------
# Filters
# --------------------------------------------------
class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__slug")
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = [
            "category",
            "min_price",
            "max_price",
        ]


# --------------------------------------------------
# Category List
# GET /api/v1/categories
# --------------------------------------------------
class CategoryListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = (
        Category.objects.filter(parent__isnull=True)
        .order_by("name")
    )

    serializer_class = CategorySerializer


# --------------------------------------------------
# Product List
# GET /api/v1/products
# --------------------------------------------------
class ProductListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    serializer_class = ProductListSerializer

    queryset = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related("images")
        .annotate(
            average_rating=Avg("reviews__rating"),
            review_count=Count("reviews"),
        )
    )

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = ProductFilter

    search_fields = [
        "name",
        "sku",
        "description",
        "ingredients",
    ]

    ordering_fields = [
        "price",
        "mrp",
        "created_at",
        "name",
        "average_rating",
    ]

    ordering = [
        "-created_at",
    ]


# --------------------------------------------------
# Product Detail
# GET /api/v1/products/<slug>
# --------------------------------------------------
class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]

    serializer_class = ProductDetailSerializer

    lookup_field = "slug"

    queryset = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related(
            "images",
            "reviews",
            "reviews__user",
        )
        .annotate(
            average_rating=Avg("reviews__rating"),
            review_count=Count("reviews"),
        )
    )


# --------------------------------------------------
# Reviews
# GET / POST
# --------------------------------------------------
class ProductReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return (
            Product.objects.get(
                id=self.kwargs["product_id"]
            )
            .reviews.select_related("user")
            .all()
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            product_id=self.kwargs["product_id"],
        )