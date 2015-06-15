# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0023_remove_item_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='main_image',
            field=models.ImageField(upload_to=b'images/materials/%Y/%m/', verbose_name='Main Image'),
        ),
    ]
