# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0068_auto_20150708_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='icon',
            field=models.ForeignKey(default=None, blank=True, to='materials.Icon'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='icon',
            field=models.ForeignKey(default=None, blank=True, to='materials.Icon'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 8, 13, 44, 55, 929977, tzinfo=utc), verbose_name='Year release'),
        ),
    ]