# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0073_auto_20150709_0749'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300, verbose_name='Title genre')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 9, 12, 51, 19, 677447, tzinfo=utc), verbose_name='Year release'),
        ),
        migrations.AddField(
            model_name='item',
            name='genre',
            field=models.ManyToManyField(related_name='items', verbose_name='Genre', to='materials.Genre'),
        ),
    ]
