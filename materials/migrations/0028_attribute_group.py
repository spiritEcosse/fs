# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0027_auto_20150622_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='group',
            field=models.ManyToManyField(related_name='attributes', verbose_name='Group', to='materials.Group', blank=True),
        ),
    ]
