# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0007_auto_20150416_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='rating',
            field=models.ImageField(upload_to=b'', blank=True),
        ),
    ]
