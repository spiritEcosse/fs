# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0008_auto_20150515_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='main_group',
            field=models.ForeignKey(verbose_name='Main Group', blank=True, to='materials.Group', null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='main_image',
            field=models.ImageField(upload_to=b'images/materials/%Y/%m/', null=True, verbose_name='Main Image', blank=True),
        ),
    ]
