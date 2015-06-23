# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0028_attribute_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='group',
        ),
        migrations.AddField(
            model_name='attribute',
            name='children',
            field=models.ManyToManyField(related_name='children_rel_+', verbose_name='Group attributes', to='materials.Attribute', blank=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='groups',
            field=models.ManyToManyField(related_name='attributes', verbose_name='Group', to='materials.Group', blank=True),
        ),
    ]
