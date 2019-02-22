from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fs.settings')
app = Celery('fs')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.conf.beat_schedule = {
#     'add-every-day': {
#         'task': 'materials.tasks.parser_premiere',
#         'schedule': crontab(hour=17, minute=55)
#     },
# }
