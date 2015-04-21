# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_auto_20150416_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='icon',
            field=models.ImageField(upload_to=b'self._meta.app_label/self._meta.model_name/icon/', blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(to='materials.Group', blank=True),
        ),
    ]
