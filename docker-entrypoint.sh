#!/usr/bin/env bash
# python manage.py migrate --noinput

# python manage.py loaddata dumpdata/db.json

# python manage.py collectstatic --noinput

# python manage.py rebuild_index --noinput

if [[ $PRODUCTION == 1 ]]; then
    celery worker -A fs -E -l info &
    celery flower -A fs -E -l info &
    gunicorn fs.wsgi --log-file -
else
    python manage.py runserver 0.0.0.0:8000
fi
