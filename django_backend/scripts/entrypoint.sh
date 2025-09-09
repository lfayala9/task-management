#!/bin/sh

set -e  # que falle el script si un comando falla

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is up!"

echo "Applying migrations..."
python manage.py migrate

echo "Loading initial data..."
python manage.py shell -c 'exec(open("/app/init_data.py").read())'

echo "Starting Django..."
python manage.py runserver 0.0.0.0:8000