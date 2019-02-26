# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_auto_20190218_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2019, 2, 18, 11, 32, 59, 289830, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
