#!/bin/bash

echo "Running database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Initializing other necessary services or tasks..."

echo "Starting Gunicorn..."
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
