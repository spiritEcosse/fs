# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0063_auto_20150708_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to=b'images/materials/icon/%Y/%m/', verbose_name='Image icon', blank=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Icon',
                'verbose_name_plural': 'Icons',
            },
        ),
        migrations.AlterField(
            model_name='attribute',
            name='icon',
            field=models.ForeignKey(to='materials.Icon', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='year_release',
            field=models.DateField(default=datetime.datetime(2015, 7, 8, 13, 36, 58, 171559, tzinfo=utc), verbose_name='Year release'),
        ),
        migrations.AddField(
            model_name='group',
            name='icon',
            field=models.ForeignKey(default=None, blank=True, to='materials.Icon'),
            preserve_default=False,
        ),
    ]
