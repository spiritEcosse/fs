# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0082_auto_20150709_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='countries',
        ),
        migrations.AlterField(
            model_name='item',
            name='genre',
            field=models.ManyToManyField(related_name='items', verbose_name='Genre', to='materials.Genre', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 9, 15, 10, 14, 217698, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
