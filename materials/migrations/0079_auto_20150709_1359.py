# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0078_auto_20150709_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='countries',
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 9, 13, 59, 16, 463851, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
