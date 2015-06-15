# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0006_auto_20150515_0710'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='popular',
            field=models.BigIntegerField(default=0, verbose_name='Popular', editable=False, blank=True),
        ),
    ]
