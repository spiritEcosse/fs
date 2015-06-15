# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0020_item_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='creator',
        ),
    ]
