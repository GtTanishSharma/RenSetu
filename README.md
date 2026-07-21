# HARIT — Green Energy Directory (Django)

A full directory site: rooftop solar, wind, rainwater, EV, biogas and more.
Dealers, tools, guides and enquiries are all managed from the **admin panel** —
no code needed once it's running.

## What you can do from the admin

Log in at `/harit-admin/` and you can:
- **Site settings** — set your WhatsApp number (used by every enquiry button) and region
- **Dealers** — add/edit/remove listings, tick "Verified", assign categories
- **Categories** — the 10 green solutions (edit text, costs, subsidies, order)
- **Tools & Guides** — edit the calculators' descriptions and the articles
- **Enquiries** — every "Get Quotes" submission, saved and markable as handled
- **Supplier applications** — every "List Your Business" submission

## Run it locally (first time)

Open the folder in VS Code, then in the terminal:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env

# put a real SECRET_KEY in .env:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# paste the output into SECRET_KEY in .env

python manage.py migrate
python manage.py seed_harit       # loads the 10 solutions, 14 sample dealers, 7 tools, 6 guides
python manage.py createsuperuser  # your admin login
python manage.py runserver
```

- Site: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/harit-admin/

## BEFORE GOING LIVE — two must-do edits

1. **Your WhatsApp number.** Admin → Site settings → set `owner_whatsapp`
   (country code + number, digits only, e.g. `919812345678`).
2. **The dealers are samples.** The 14 seeded dealers use fake `90000 0000x`
   numbers. In admin → Dealers, replace them with your real onboarded suppliers,
   or delete them and add your own.

## Deploy (Render example)

1. Push to a GitHub repo.
2. Create a **PostgreSQL** instance on Render, copy its connection URL.
3. Create a **Web Service** from the repo:
   - Build command: `./build.sh`
   - Start command: `gunicorn config.wsgi`
4. Set environment variables in Render:
   - `SECRET_KEY` — a fresh random key
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = your Render URL + your domain
   - `CSRF_TRUSTED_ORIGINS` = `https://yourdomain.com`
   - `DATABASE_URL` = the Postgres URL from step 2
5. After first deploy, run `python manage.py seed_harit` and `createsuperuser`
   from the Render shell.

Free tiers on Render/Railway work for low traffic (they sleep when idle).
A small always-on VPS is ~₹300–800/month.

## Common commands

```bash
python manage.py runserver          # run locally
python manage.py seed_harit         # reload starter content
python manage.py createsuperuser    # add an admin user
python manage.py makemigrations     # after changing models
python manage.py migrate            # apply DB changes
```
