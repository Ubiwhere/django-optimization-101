#!/bin/bash

# Based on:
# https://github.com/django/djangoproject.com/blob/main/docker-entrypoint.sh


# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate


exec "$@"