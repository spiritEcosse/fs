# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0016_auto_20150530_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='sort',
            field=models.IntegerField(default=0, verbose_name='Sort', blank=True),
        ),
    ]
