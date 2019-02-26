# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0011_item_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='original_image',
            field=models.URLField(
                verbose_name='Link image from original source'),
            preserve_default=False,
        ),
    ]
