# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0058_auto_20150707_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='main_group',
            field=models.ForeignKey(related_name='items_main_group', verbose_name='Main Group', to='materials.Group'),
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 8, 12, 41, 8, 698419, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
