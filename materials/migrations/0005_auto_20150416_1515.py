# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_auto_20150416_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(blank=True, to='materials.Group', null=True),
        ),
    ]
