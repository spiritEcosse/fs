# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0009_auto_20150420_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='rating',
        ),
    ]
