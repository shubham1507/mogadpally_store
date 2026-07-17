# Mogadpally Brothers — Postman Collection

Tests every implemented REST endpoint in `mogadpally_store` end-to-end, with tokens and IDs
chained automatically between requests via Postman test scripts — you don't need to manually
copy an access token or product ID between calls.

## Files

- `Mogadpally_Brothers_API.postman_collection.json` — 35 requests across 7 folders
- `Mogadpally_Brothers_API.postman_environment.json` — variables (base_url, tokens, IDs)
- `reports/` — output directory for Newman HTML/JSON reports (gitignored except this note)

## Setup

1. Postman → **Import** → select both JSON files (collection + environment)
2. Top-right environment dropdown → select **"Mogadpally Brothers - Local"**
3. Make sure the Django server is running: `python manage.py runserver` (default `http://localhost:8000`, matching `base_url`)
4. If your admin login should be tested, fill in `admin_email` / `admin_password` in the environment with your `createsuperuser` credentials — otherwise leave blank and skip "Login (Admin)".

## Run order (matters — later folders depend on earlier ones)

Run folders top to bottom, or use **Collection Runner** to run the whole collection in sequence:

1. **01 - Auth → Signup** (or **Login**, if the user already exists) — saves `access_token`, `refresh_token`
2. **02 - Catalog → List Products** — saves `product_id`, `product_id_2`, `product_slug` from real seeded data
3. **01 - Auth → Add Address** — saves `address_id` (needed for Checkout)
4. **03 - Cart → Add Item to Cart** / **Add Second Item to Cart**
5. **05 - Orders → Create Order (Checkout)** — saves `order_id`, needs cart items + `address_id` from steps above
6. **06 - Payments → Create Payment Intent** — needs `order_id`; will fail against Razorpay's real API unless valid keys are in your backend's `.env`
7. Everything else (Wishlist, reviews, cancel, address update/delete) can run independently once you're authenticated

**Note on "Delete Address"** and **"Clear Cart"** — these are destructive by design (they test the delete path). They're placed at the end of their folders intentionally; running them early will break the Orders folder's dependency on `address_id` / cart contents. Re-run **Add Address** / **Add Item to Cart** afterward if you need to continue testing Orders.

## What's NOT covered (by design, not oversight)

- **`07 - Admin`** contains one placeholder request. The admin panel in this project is Django's
  built-in HTML admin (`apps/*/admin.py`), not a REST API — there's nothing else to test with
  Postman here. Product/order management is verified by hand in the browser at `/admin/`.
- **Webhook** request in `06 - Payments` is reference-only. Razorpay signs webhook calls
  server-side using your webhook secret over the exact raw request body — Postman can't
  replicate that signature. Use Razorpay's dashboard test-webhook feature, or the
  `razorpay` Python SDK's test utilities, to fire a properly signed request at
  `/api/v1/payments/webhook`.

## Running via Newman (CLI / CI)

```bash
npm install -g newman newman-reporter-htmlextra

newman run postman/Mogadpally_Brothers_API.postman_collection.json \
  -e postman/Mogadpally_Brothers_API.postman_environment.json \
  -r cli,htmlextra \
  --reporter-htmlextra-export postman/reports/report.html
```

This runs all 35 requests in folder order and writes a self-contained HTML report to
`postman/reports/report.html`. Exit code is non-zero if any `pm.test()` assertion fails,
so it's safe to wire into a GitHub Actions step:

```yaml
- name: Run API tests
  run: |
    newman run postman/Mogadpally_Brothers_API.postman_collection.json \
      -e postman/Mogadpally_Brothers_API.postman_environment.json \
      -r cli,junit \
      --reporter-junit-export postman/reports/results.xml
```

(`newman-reporter-junit` ships with `newman` by default — no extra install needed for the JUnit variant, only `htmlextra` needs a separate package.)

## Maintaining this collection going forward

Every test currently only asserts a 2xx status code — deliberately minimal so the collection
stays in sync with a backend that's still evolving. As specific endpoints stabilize, add
stronger assertions (response shape, specific field values) directly in that request's **Tests**
tab in Postman, then re-export the collection JSON over this file. Keep this whole `postman/`
folder under version control in the main repo so collection changes are reviewed alongside the
API changes that prompted them.
