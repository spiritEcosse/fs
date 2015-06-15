# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0015_auto_20150530_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='sort',
            field=models.IntegerField(default=0, null=True, verbose_name='Sort', blank=True),
        ),
    ]
