# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0025_item_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='like',
            field=models.BigIntegerField(default=0, verbose_name='Like'),
        ),
        migrations.AddField(
            model_name='item',
            name='not_like',
            field=models.BigIntegerField(default=0, verbose_name='Not like'),
        ),
    ]
