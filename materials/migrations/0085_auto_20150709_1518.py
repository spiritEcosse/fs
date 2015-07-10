# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0084_auto_20150709_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 9, 15, 18, 30, 627925, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
