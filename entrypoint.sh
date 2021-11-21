#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn mokuton.wsgi:application --bind 0.0.0.0:8000 --timeout 30 --workers 4 --keep-alive 1 --log-level=debug

# python manage.py run_huey
