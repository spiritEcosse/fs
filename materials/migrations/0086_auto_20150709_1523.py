# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '__first__'),
        ('materials', '0085_auto_20150709_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='countries',
            field=models.ManyToManyField(to='cities.Country', verbose_name='Countries production'),
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 9, 15, 23, 22, 419819, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
