web: gunicorn fs.wsgi --log-file -
worker: celery beat -A fs -E -l debug
