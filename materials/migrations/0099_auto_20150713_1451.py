# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '__first__'),
        ('materials', '0098_auto_20150713_1450'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExtendCountry',
        ),
        migrations.CreateModel(
            name='ExCountry',
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
            field=models.ManyToManyField(to='materials.ExCountry', verbose_name='Countries production'),
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 13, 14, 51, 21, 213953, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
