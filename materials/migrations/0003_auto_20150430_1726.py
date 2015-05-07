# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_auto_20150430_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemattributerelationship',
            name='attribute',
            field=models.ForeignKey(related_name='item_attributes', to='materials.Attribute'),
        ),
    ]
