#!/bin/sh

python manage.py makemigrations --noinput && python manage.py migrate --noinput

python manage.py loaddata dumpdata/db.json

python manage.py collectstatic --noinput

python manage.py rebuild_index --noinput

gunicorn fs.wsgi --log-file -
