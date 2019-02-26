# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_auto_20150727_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenreTree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='materials.GenreTree', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 10, 21, 8, 22, 24, 945514, tzinfo=utc), verbose_name='Year release'),
        ),
    ]
