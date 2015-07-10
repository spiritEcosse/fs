# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0070_auto_20150708_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='group',
            name='icon',
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 8, 13, 46, 38, 372403, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
