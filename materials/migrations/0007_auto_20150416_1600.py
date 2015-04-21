# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0006_auto_20150416_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='icon',
            field=models.ImageField(upload_to=b'self._meta.app_label/self._meta.model_name/icon/', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(size=None, base_field=models.ImageField(upload_to=b'self._meta.app_label/self._meta.model_name/images/%Y/%m/%d/'), blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='main_image',
            field=models.ImageField(upload_to=b'self._meta.app_label/self._meta.model_name/main_image/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='item',
            name='trailer_image',
            field=models.ImageField(upload_to=b'self._meta.app_label/self._meta.model_name/trailer_image/', blank=True),
        ),
    ]
