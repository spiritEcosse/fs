# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0036_auto_20150624_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='sort',
            field=models.IntegerField(default=0, verbose_name='Sort', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 6, 27, 9, 3, 18, 407290, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
