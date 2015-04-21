# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_auto_20150416_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='date_create',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 16, 14, 36, 57, 245371, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='date_last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 16, 14, 37, 47, 494523, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='enable',
            field=models.BooleanField(default=True),
        ),
    ]
