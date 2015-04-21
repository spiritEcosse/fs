# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='structure',
            field=models.CharField(default=b'standalone', max_length=10, verbose_name='Product structure', choices=[(b'standalone', 'Stand-alone product'), (b'parent', 'Parent product'), (b'child', 'Child product')]),
        ),
    ]
