# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0011_item_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='rating',
            field=models.ImageField(upload_to=b'', editable=False, blank=True),
        ),
    ]
