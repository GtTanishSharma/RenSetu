#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_harit
python manage.py import_dealers RenSetu_Dealers_Formatted.xlsx
python manage.py createsuperuser --noinput || true
python manage.py shell -c "from django.contrib.sites.models import Site; Site.objects.update_or_create(id=1, defaults={'domain': 'rensetu.in', 'name': 'RenSetu'})"