# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_auto_20150727_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2019, 2, 18, 11, 22, 45, 22122, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
