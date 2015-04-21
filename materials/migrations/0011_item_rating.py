# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0010_remove_item_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='rating',
            field=django.contrib.postgres.fields.hstore.HStoreField(default=''),
            preserve_default=False,
        ),
    ]
