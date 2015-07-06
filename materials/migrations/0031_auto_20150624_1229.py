# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0030_auto_20150622_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemattributerelationship',
            name='attribute_values',
            field=models.ManyToManyField(to='materials.AttributeValue', blank=True),
        ),
    ]
