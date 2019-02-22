#!/usr/bin/env bash

python manage.py makemigrations --noinput && python manage.py migrate --noinput

python manage.py loaddata dumpdata/db.json

python manage.py collectstatic --noinput

python manage.py rebuild_index --noinput

# if [[ $PRODUCTION == 1 ]]; then
#     gunicorn fs.wsgi --log-file -
# else
#     python manage.py runserver 0.0.0.0:8000
# fi
