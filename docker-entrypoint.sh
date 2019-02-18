#!/bin/sh

python manage.py makemigrations --noinput && python manage.py migrate --noinput

python manage.py collectstatic --noinput

python manage.py rebuild_index

python manage.py runserver 0.0.0.0:8000
