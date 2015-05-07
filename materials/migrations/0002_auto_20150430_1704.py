# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemattributerelationship',
            name='attribute',
            field=models.ForeignKey(related_name='item_attr_relate', to='materials.Attribute'),
        ),
    ]
