# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0088_auto_20150710_0740'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='genre',
            new_name='genres',
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 10, 7, 59, 51, 848935, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
