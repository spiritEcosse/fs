# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_auto_20190218_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2019, 2, 18, 11, 35, 42, 486066, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
