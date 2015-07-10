# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0054_auto_20150706_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='video',
            field=models.TextField(default='', verbose_name=b'Video'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 6, 16, 14, 34, 393640, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
