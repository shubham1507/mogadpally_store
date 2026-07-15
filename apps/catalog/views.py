import django_filters
from rest_framework import generics, permissions
from .models import Category, Product
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer, ReviewSerializer,
)


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    search = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["category", "min_price", "max_price", "search"]


class CategoryListView(generics.ListAPIView):
    """GET /api/v1/categories"""
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    """GET /api/v1/products?category=&min_price=&max_price=&search=&page="""
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.filter(is_active=True).prefetch_related("images")
    serializer_class = ProductListSerializer
    filterset_class = ProductFilter
    ordering_fields = ["price", "created_at"]


class ProductDetailView(generics.RetrieveAPIView):
    """GET /api/v1/products/:slug"""
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"


class ProductReviewListCreateView(generics.ListCreateAPIView):
    """GET (public) / POST (auth) /api/v1/products/:product_id/reviews"""
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return Product.objects.get(id=self.kwargs["product_id"]).reviews.all()

    def perform_create(self, serializer):
        # TODO: verify user has an order containing this product before allowing review
        serializer.save(user=self.request.user, product_id=self.kwargs["product_id"])
