# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0066_auto_20150708_1343'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Icon',
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 8, 13, 44, 16, 587498, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
