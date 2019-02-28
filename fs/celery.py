from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fs.settings')
app = Celery('fs')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'parser_premiere': {
        'task':
        'materials.tasks.parser_premiere',
        'schedule':
        crontab(
            hour=os.environ.get('PARSER_PREMIERE_HOUR'),
            minute=os.environ.get('PARSER_PREMIERE_MINUTE')),
    },
}
