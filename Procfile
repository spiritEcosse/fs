web: gunicorn fs.wsgi --log-file -
worker: celery worker -A fs -l debug
