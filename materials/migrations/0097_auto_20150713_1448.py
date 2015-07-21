# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '__first__'),
        ('materials', '0096_auto_20150713_1448'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExCountry',
        ),
        migrations.CreateModel(
            name='ExtendCountry',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('cities.country',),
        ),
        migrations.AlterField(
            model_name='item',
            name='countries',
            field=models.ManyToManyField(to='materials.ExtendCountry', verbose_name='Countries production'),
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 13, 14, 48, 55, 743023, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
