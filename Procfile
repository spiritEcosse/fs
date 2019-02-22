web: gunicorn fs.wsgi --log-file -
worker: celery worker -A fs -E -l info
flower: celery flower -A fs -E -l info
redis: redis-server
