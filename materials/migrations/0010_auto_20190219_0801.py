# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0009_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genretree',
            name='parent',
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(auto_now=True, verbose_name='Year release'),
        ),
        migrations.DeleteModel(name='GenreTree', ),
    ]
