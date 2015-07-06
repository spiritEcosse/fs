# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0032_auto_20150624_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='parent',
        ),
    ]
