web: gunicorn fs.wsgi --log-file -
beat: celery beat -A fs -l debug
worker: celery worker -A fs -l debug
