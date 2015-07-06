# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0047_remove_item_year_release'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 6, 27, 10, 40, 3, 355738, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
