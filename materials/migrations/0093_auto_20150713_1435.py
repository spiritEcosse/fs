# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '__first__'),
        ('materials', '0092_auto_20150713_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extendcountry',
            name='country_ptr',
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
            field=models.DateField(default=datetime.datetime(2015, 7, 13, 14, 35, 43, 345815, tzinfo=utc), verbose_name='Year release'),
        ),
        migrations.DeleteModel(
            name='ExtendCountry',
        ),
    ]
