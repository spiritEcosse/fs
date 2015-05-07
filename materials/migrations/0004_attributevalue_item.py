# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_auto_20150430_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributevalue',
            name='item',
            field=models.ForeignKey(related_name='attribute_values', to='materials.Item', null=True),
        ),
    ]
