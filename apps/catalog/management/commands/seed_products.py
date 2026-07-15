"""
Seeds realistic Ayurvedic product data.

Usage:
    python manage.py seed_products
    python manage.py seed_products --flush
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.catalog.models import Category, Product


CATEGORIES = [
    {"name": "Immunity & Wellness", "slug": "immunity-wellness"},
    {"name": "Digestive Care", "slug": "digestive-care"},
    {"name": "Skin & Hair Care", "slug": "skin-hair-care"},
    {"name": "Stress & Sleep", "slug": "stress-sleep"},
    {"name": "Joint & Pain Relief", "slug": "joint-pain-relief"},
]

PRODUCTS = [
    {
        "name": "Chyawanprash — Classic",
        "sku": "MB-CHY-500",
        "category": "immunity-wellness",
        "price": 340,
        "mrp": 400,
        "stock": 120,
        "weight_grams": 500,
        "ingredients": "Amla, Ashwagandha, Giloy, honey, ghee, and a blend of 40+ herbs",
        "benefits": "Daily immunity support, rasayana (rejuvenative) tonic, respiratory health",
        "description": "Traditional Chyawanprash prepared using our forefathers' original recipe, slow-cooked in small batches.",
    },
    {
        "name": "Ashwagandha Capsules",
        "sku": "MB-ASH-60CAP",
        "category": "stress-sleep",
        "price": 280,
        "mrp": 320,
        "stock": 200,
        "weight_grams": 60,
        "ingredients": "Standardized Withania somnifera root extract (KSM-66 equivalent, 500mg/capsule)",
        "benefits": "Stress reduction, better sleep quality, energy and stamina support",
        "description": "60 vegetarian capsules of pure Ashwagandha root extract, lab-tested for potency.",
    },
    {
        "name": "Triphala Churna",
        "sku": "MB-TRI-200",
        "category": "digestive-care",
        "price": 150,
        "mrp": 180,
        "stock": 300,
        "weight_grams": 200,
        "ingredients": "Amalaki, Bibhitaki, Haritaki (equal proportions)",
        "benefits": "Digestive regularity, gentle detoxification, gut health",
        "description": "Classic three-fruit powder blend, stone-ground the traditional way.",
    },
    {
        "name": "Neem-Tulsi Face Pack",
        "sku": "MB-NTF-100",
        "category": "skin-hair-care",
        "price": 190,
        "mrp": 220,
        "stock": 150,
        "weight_grams": 100,
        "ingredients": "Neem leaf powder, Tulsi, Multani mitti, Sandalwood",
        "benefits": "Acne control, skin purification, natural glow",
        "description": "Herbal face pack for oily and acne-prone skin, mix with rosewater.",
    },
    {
        "name": "Mahanarayan Oil",
        "sku": "MB-MNO-200ML",
        "category": "joint-pain-relief",
        "price": 260,
        "mrp": 300,
        "stock": 90,
        "weight_grams": 220,
        "ingredients": "Sesame oil base with Bala, Ashwagandha, and 20+ therapeutic herbs",
        "benefits": "Joint and muscle pain relief, improves mobility, post-exercise recovery",
        "description": "Classical Ayurvedic oil for external application, warmed before massage.",
    },
    {
        "name": "Brahmi-Shankhpushpi Syrup",
        "sku": "MB-BSS-200ML",
        "category": "stress-sleep",
        "price": 210,
        "mrp": 240,
        "stock": 110,
        "weight_grams": 220,
        "ingredients": "Brahmi, Shankhpushpi, Jatamansi in a honey base",
        "benefits": "Cognitive clarity, calm focus, supports restful sleep",
        "description": "A gentle nervine tonic taken twice daily, suitable for students and professionals.",
    },
    {
        "name": "Giloy Ghanvati Tablets",
        "sku": "MB-GIL-60TAB",
        "category": "immunity-wellness",
        "price": 165,
        "mrp": 190,
        "stock": 250,
        "weight_grams": 50,
        "ingredients": "Concentrated Tinospora cordifolia (Giloy) extract",
        "benefits": "Immunity building, fever recovery support, general wellness",
        "description": "60 tablets of concentrated Giloy extract in convenient tablet form.",
    },
    {
        "name": "Bhringraj Hair Oil",
        "sku": "MB-BHO-200ML",
        "category": "skin-hair-care",
        "price": 230,
        "mrp": 260,
        "stock": 140,
        "weight_grams": 220,
        "ingredients": "Bhringraj, Amla, Coconut oil base, Curry leaf extract",
        "benefits": "Reduces hair fall, promotes growth, nourishes scalp",
        "description": "Cold-pressed hair oil for regular use, light non-greasy formula.",
    },
]


class Command(BaseCommand):
    help = "Seed realistic Ayurvedic catalog data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all categories and products before seeding",
        )

    def handle(self, *args, **options):

        if options["flush"]:
            confirm = input(
                "\nThis will DELETE all catalog data.\nType 'yes' to continue: "
            )

            if confirm.lower() != "yes":
                self.stdout.write(self.style.WARNING("Operation cancelled."))
                return

            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing catalog deleted.\n"))

        self.stdout.write(self.style.HTTP_INFO("Seeding categories..."))

        category_map = {}

        for c in CATEGORIES:
            category, created = Category.objects.update_or_create(
                slug=c["slug"],
                defaults={
                    "name": c["name"],
                },
            )

            category_map[c["slug"]] = category

            if created:
                self.stdout.write(self.style.SUCCESS(f"  ✔ Created {category.name}"))
            else:
                self.stdout.write(f"  • Updated {category.name}")

        self.stdout.write("")
        self.stdout.write(self.style.HTTP_INFO("Seeding products..."))

        created_count = 0
        updated_count = 0

        for p in PRODUCTS:

            slug = slugify(p["name"])

            # Handle slug conflicts (e.g. SKU changed)
            existing_slug = Product.objects.filter(slug=slug).exclude(sku=p["sku"]).first()

            if existing_slug:
                existing_slug.sku = p["sku"]

            product, created = Product.objects.update_or_create(
                sku=p["sku"],
                defaults={
                    "name": p["name"],
                    "slug": slug,
                    "category": category_map[p["category"]],
                    "price": p["price"],
                    "mrp": p["mrp"],
                    "stock_quantity": p["stock"],
                    "weight_grams": p["weight_grams"],
                    "ingredients": p["ingredients"],
                    "ayurvedic_benefits": p["benefits"],
                    "description": p["description"],
                    "is_active": True,
                },
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  ✔ Created {product.name}"))
            else:
                updated_count += 1
                self.stdout.write(f"  • Updated {product.name}")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(
            self.style.SUCCESS(
                f"Categories : {Category.objects.count()}\n"
                f"Products   : {Product.objects.count()}\n"
                f"Created    : {created_count}\n"
                f"Updated    : {updated_count}"
            )
        )
        self.stdout.write(self.style.SUCCESS("=" * 60))