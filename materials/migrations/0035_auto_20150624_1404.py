# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0034_attribute_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='parent',
            field=models.ForeignKey(related_name='children', verbose_name='Parent', blank=True, to='materials.Attribute'),
        ),
    ]
