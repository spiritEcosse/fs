# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0046_auto_20150627_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='year_release',
        ),
    ]
