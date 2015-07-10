# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0071_auto_20150708_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='icon',
            field=models.ForeignKey(blank=True, to='materials.Icon', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='icon',
            field=models.ForeignKey(blank=True, to='materials.Icon', null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 8, 13, 46, 52, 277873, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
