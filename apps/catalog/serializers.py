from rest_framework import serializers

from .models import Category, Product, ProductImage, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "parent",
            "description",
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "is_primary",
            "sort_order",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]


class ProductListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer used for product listing pages.
    """

    primary_image = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "mrp",
            "in_stock",
            "primary_image",
            "category",
            "average_rating",
            "review_count",
        ]

    def get_primary_image(self, obj):
        image = (
            obj.images.filter(is_primary=True).first()
            or obj.images.first()
        )

        if image:
            return image.image.url

        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer used for product detail page.
    """

    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "sku",
            "category",
            "description",
            "ayurvedic_benefits",
            "ingredients",
            "weight_grams",
            "price",
            "mrp",
            "stock_quantity",
            "in_stock",
            "average_rating",
            "review_count",
            "images",
            "reviews",
        ]