# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0033_remove_attribute_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='parent',
            field=models.ForeignKey(related_name='attributes', default=6, verbose_name='Parent', blank=True, to='materials.Attribute'),
            preserve_default=False,
        ),
    ]
