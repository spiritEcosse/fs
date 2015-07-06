# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0048_item_year_release'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='countries',
            field=django.contrib.postgres.fields.ArrayField(default=[], base_field=models.CharField(max_length=200), verbose_name='countries', size=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 6, 27, 10, 40, 55, 825587, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
