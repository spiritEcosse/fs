# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '__first__'),
        ('materials', '0091_auto_20150713_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendCountry',
            fields=[
                ('country_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cities.Country')),
            ],
            options={
                'abstract': False,
            },
            bases=('cities.country',),
        ),
        migrations.RemoveField(
            model_name='excountry',
            name='country_ptr',
        ),
        migrations.AlterField(
            model_name='item',
            name='countries',
            field=models.ManyToManyField(to='materials.ExtendCountry', verbose_name='Countries production'),
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 13, 14, 32, 26, 36421, tzinfo=utc), verbose_name='Year release'),
        ),
        migrations.DeleteModel(
            name='ExCountry',
        ),
    ]
