# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0043_auto_20150627_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='countries',
            field=django.contrib.postgres.fields.ArrayField(default=[], base_field=models.CharField(max_length=200), verbose_name='countries', size=None),
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 6, 27, 10, 38, 22, 945925, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
