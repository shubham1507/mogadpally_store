from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.catalog.models import Category, Product


class Command(BaseCommand):
    help = "Seed sample categories and products for admin CRUD testing"

    def handle(self, *args, **kwargs):
        categories = [
            {
                "name": "Stress & Sleep",
                "description": "Products that help reduce stress and improve sleep.",
            },
            {
                "name": "Immunity",
                "description": "Immunity boosting Ayurvedic products.",
            },
            {
                "name": "Digestive Care",
                "description": "Products for better digestion.",
            },
            {
                "name": "Women's Wellness",
                "description": "Women's health products.",
            },
            {
                "name": "Hair Care",
                "description": "Natural hair care products.",
            },
        ]

        category_map = {}

        for data in categories:
            category, created = Category.objects.get_or_create(
                slug=slugify(data["name"]),
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                },
            )
            category_map[data["name"]] = category

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Category: {category.name}"))
            else:
                self.stdout.write(f"Category already exists: {category.name}")

        products = [
            {
                "name": "Ashwagandha Capsules",
                "sku": "MB001",
                "category": "Stress & Sleep",
                "price": Decimal("499.00"),
                "mrp": Decimal("599.00"),
                "stock": 100,
                "weight": 60,
            },
            {
                "name": "Brahmi Tablets",
                "sku": "MB002",
                "category": "Stress & Sleep",
                "price": Decimal("399.00"),
                "mrp": Decimal("499.00"),
                "stock": 80,
                "weight": 60,
            },
            {
                "name": "Giloy Juice",
                "sku": "MB003",
                "category": "Immunity",
                "price": Decimal("299.00"),
                "mrp": Decimal("349.00"),
                "stock": 150,
                "weight": 500,
            },
            {
                "name": "Tulsi Drops",
                "sku": "MB004",
                "category": "Immunity",
                "price": Decimal("199.00"),
                "mrp": Decimal("249.00"),
                "stock": 200,
                "weight": 30,
            },
            {
                "name": "Triphala Powder",
                "sku": "MB005",
                "category": "Digestive Care",
                "price": Decimal("249.00"),
                "mrp": Decimal("299.00"),
                "stock": 90,
                "weight": 250,
            },
            {
                "name": "Amla Hair Oil",
                "sku": "MB006",
                "category": "Hair Care",
                "price": Decimal("349.00"),
                "mrp": Decimal("399.00"),
                "stock": 70,
                "weight": 200,
            },
            {
                "name": "Shatavari Capsules",
                "sku": "MB007",
                "category": "Women's Wellness",
                "price": Decimal("449.00"),
                "mrp": Decimal("549.00"),
                "stock": 60,
                "weight": 60,
            },
        ]

        created_count = 0

        for item in products:
            _, created = Product.objects.get_or_create(
                sku=item["sku"],
                defaults={
                    "name": item["name"],
                    "slug": slugify(item["name"]),
                    "category": category_map[item["category"]],
                    "description": f"{item['name']} for admin CRUD testing.",
                    "ayurvedic_benefits": "Natural Ayurvedic formulation.",
                    "ingredients": "Herbal ingredients.",
                    "weight_grams": item["weight"],
                    "price": item["price"],
                    "mrp": item["mrp"],
                    "stock_quantity": item["stock"],
                    "is_active": True,
                },
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created Product: {item['name']}")
                )
            else:
                self.stdout.write(f"Product already exists: {item['name']}")

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Done! {len(category_map)} categories available, "
                f"{created_count} new products created."
            )
        )