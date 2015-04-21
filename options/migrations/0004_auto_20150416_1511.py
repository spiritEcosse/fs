# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('options', '0003_auto_20150416_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='icon',
            field=models.ImageField(upload_to=b'icon/'),
        ),
    ]
