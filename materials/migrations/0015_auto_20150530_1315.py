# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0014_auto_20150527_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='groups',
            field=models.ManyToManyField(related_name='items', verbose_name='Group', to='materials.Group', blank=True),
        ),
    ]
