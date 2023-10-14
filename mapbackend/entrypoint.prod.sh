#!/bin/sh
python manage.py collectstatic --no-input --clear
python manage.py migrate
gunicorn mapbackend.wsgi:application --bind 0.0.0.0:8000
exec "$@"
