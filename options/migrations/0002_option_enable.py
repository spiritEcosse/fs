# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('options', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='enable',
            field=models.BooleanField(default=True),
        ),
    ]
