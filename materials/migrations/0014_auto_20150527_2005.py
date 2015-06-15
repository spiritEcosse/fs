# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0013_group_enable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemattributerelationship',
            name='item',
            field=models.ForeignKey(related_name='item_attr', to='materials.Item'),
        ),
    ]
