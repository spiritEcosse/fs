# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0009_auto_20150519_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='groups',
            field=models.ManyToManyField(related_name='items', null=True, verbose_name='Group', to='materials.Group', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='main_group',
            field=models.ForeignKey(default=None, verbose_name='Main Group', to='materials.Group'),
            preserve_default=False,
        ),
    ]
