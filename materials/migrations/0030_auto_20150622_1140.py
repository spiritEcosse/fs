# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0029_auto_20150622_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='image',
        ),
        migrations.AddField(
            model_name='attribute',
            name='icon',
            field=models.CharField(blank=True, max_length=100, choices=[(b'asterisk', b'asterisk'), (b'music', b'music'), (b'th', b'th'), (b'th-list', b'th-list'), (b'ok', b'ok'), (b'star-empty', b'star-empty'), (b'film', b'film'), (b'user', b'user')]),
        ),
    ]
