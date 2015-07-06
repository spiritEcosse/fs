# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0044_auto_20150627_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='countries',
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 6, 27, 10, 38, 56, 331628, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
