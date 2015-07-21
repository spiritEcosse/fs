# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0105_auto_20150713_1511'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProxyModelCountry',
        ),
        migrations.AlterField(
            model_name='item',
            name='countries',
            field=models.ManyToManyField(to='cities.Country', verbose_name='Countries production'),
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 13, 15, 11, 50, 61399, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
