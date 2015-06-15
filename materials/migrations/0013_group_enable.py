# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0012_itemimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='enable',
            field=models.BooleanField(default=True, verbose_name='Enable'),
        ),
    ]
