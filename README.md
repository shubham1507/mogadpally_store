# Mogadpally Brothers — backend

Django REST Framework backend for the online store. Matches `schema.sql` and `api-contract.md`
delivered earlier — model fields mirror those tables 1:1.

## Project layout

```
config/           Django settings, root urls, wsgi
apps/
  users/          custom user model (email login), addresses, JWT auth endpoints
  catalog/        categories, products, images, reviews — also home of the Django admin
                   product-management UI (apps/catalog/admin.py)
  cart/           cart + cart items + wishlist (same domain, one app)
  orders/         checkout, order history, cancellation, coupons
  payments/       Razorpay order-intent creation + webhook handling
```

## Local setup (Windows CMD, matching your usual workflow)

```cmd
cd D:\SNJ\My_Prj\mogadpally_store
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` with your local Postgres credentials, then:

```cmd
py manage.py migrate
py manage.py createsuperuser
py manage.py seed_products
py manage.py runserver
```

Migrations are already generated and included — validated against a live SQLite run with real
Ayurvedic product data before this was handed to you (8 products across 5 categories, confirmed
via `GET /api/v1/products`, `/api/v1/categories`, and category-filtered queries). You only need
`migrate`, not `makemigrations`, unless you change a model.

`seed_products` loads 8 realistic sample products (Chyawanprash, Ashwagandha, Triphala, etc.)
so you have real-looking data to check the admin panel and API against instead of typing test
entries by hand. Run `py manage.py seed_products --flush` to wipe and reseed.

Django admin (your friend's product/order management UI) is at `http://localhost:8000/admin/`.
API root is `http://localhost:8000/api/v1/`.

## What's scaffolded vs. what's a TODO

**Working end-to-end:**
- Signup / JWT login / refresh
- Product listing with category/price/search filters, product detail, reviews
- Cart add/update/remove, wishlist add/remove
- Order creation from cart with a row-locked, transactional stock decrement
  (prevents overselling the last unit under concurrent checkouts)
- Coupon validation on checkout
- Razorpay order-intent creation + webhook with signature verification and idempotent processing
- Django admin wired for products, categories, orders, coupons

**Marked `# TODO` in code — needs your input before going live:**
- Email verification send (signup currently creates a verified-pending user but doesn't send mail — pick an email provider, e.g. SES or SendGrid)
- Shipping cost calculation (currently hardcoded to 0)
- Review eligibility check (currently anyone can review; should verify a completed order first)
- Abandoned-order stock release job (a Celery/cron task to restock orders that stay `unpaid` past a timeout)

## Next steps

1. `py manage.py makemigrations && py manage.py migrate` and confirm tables match `schema.sql`
2. Load a few test products via the Django admin, hit `GET /api/v1/products` to confirm the API works
3. Wire up the Next.js frontend against these endpoints
4. Fill in the four TODOs above before production
