# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0010_auto_20190219_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='pub_date',
            field=models.DateTimeField(verbose_name=b'PubDate'),
            preserve_default=False,
        ),
    ]
