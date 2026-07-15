from django.contrib import admin
from .models import Category, Product, ProductImage, Review


# -------------------------
# Product Images Inline
# -------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = (
        "image",
        "is_primary",
        "sort_order",
    )


# -------------------------
# Category Admin
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent",
        "slug",
    )

    search_fields = (
        "name",
        "slug",
    )

    list_filter = (
        "parent",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "name",
    )


# -------------------------
# Product Admin
# -------------------------

from django.db.models import Count

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "sku",
        "category",
        "stock_quantity",
        "price",
        "mrp",
        "discount_percent",
        "stock_status",
        "image_count",
        "review_count",
        "is_active",
        "created_at",
    )

    list_filter = (
        "category",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "sku",
        "slug",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    date_hierarchy = "created_at"

    list_editable = (
        "price",
        "stock_quantity",
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    inlines = [
        ProductImageInline,
    ]

    actions = (
        "mark_active",
        "mark_inactive",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "sku",
                    "category",
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "price",
                    "mrp",
                )
            },
        ),
        (
            "Inventory",
            {
                "fields": (
                    "stock_quantity",
                    "is_active",
                    "weight_grams",
                )
            },
        ),
        (
            "Product Details",
            {
                "fields": (
                    "description",
                    "ingredients",
                    "ayurvedic_benefits",
                )
            },
        ),
        (
            "Audit",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return (
            queryset.select_related("category")
            .annotate(
                total_images=Count("images", distinct=True),
                total_reviews=Count("reviews", distinct=True),
            )
        )

    @admin.display(description="Discount")
    def discount_percent(self, obj):
        if obj.mrp and obj.mrp > 0:
            discount = ((obj.mrp - obj.price) / obj.mrp) * 100
            return f"{discount:.0f}%"
        return "-"

    @admin.display(boolean=True, description="In Stock")
    def stock_status(self, obj):
        return obj.stock_quantity > 0

    @admin.display(description="Images")
    def image_count(self, obj):
        return obj.total_images

    @admin.display(description="Reviews")
    def review_count(self, obj):
        return obj.total_reviews

    @admin.action(description="Mark selected products as Active")
    def mark_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f"{updated} product(s) marked as Active."
        )

    @admin.action(description="Mark selected products as Inactive")
    def mark_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f"{updated} product(s) marked as Inactive."
        )
# -------------------------
# Review Admin
# -------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "user",
        "rating",
        "created_at",
    )

    search_fields = (
        "product__name",
        "user__username",
    )

    list_filter = (
        "rating",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )