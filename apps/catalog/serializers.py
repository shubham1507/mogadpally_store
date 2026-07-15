from rest_framework import serializers
from .models import Category, Product, ProductImage, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "description"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_primary", "sort_order"]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "rating", "comment", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight — used for listing/filter pages."""
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price", "mrp", "in_stock", "primary_image", "category"]

    def get_primary_image(self, obj):
        img = obj.images.filter(is_primary=True).first() or obj.images.first()
        return img.image.url if img else None


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "sku", "category", "description",
            "ayurvedic_benefits", "ingredients", "weight_grams",
            "price", "mrp", "stock_quantity", "in_stock", "images", "reviews",
        ]
