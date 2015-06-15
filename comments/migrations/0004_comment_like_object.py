# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20150612_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='like_object',
            field=models.BooleanField(default=True, verbose_name='Like'),
            preserve_default=False,
        ),
    ]
