# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0064_auto_20150708_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icon',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 8, 13, 41, 1, 119648, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
