# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0031_auto_20150624_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='children',
        ),
        migrations.AddField(
            model_name='attribute',
            name='parent',
            field=models.ForeignKey(related_name='attributes', default='', verbose_name='Parent', blank=True, to='materials.Attribute'),
            preserve_default=False,
        ),
    ]
