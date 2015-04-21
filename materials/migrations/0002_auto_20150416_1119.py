# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('options', '0001_initial'),
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('origin_title', models.CharField(max_length=100)),
                ('main_image', models.ImageField(upload_to=b'self._meta.app_label/self._meta.model_name/main_image/%Y/%m/%d/')),
                ('trailer_link', models.URLField(blank=True)),
                ('trailer_image', models.ImageField(upload_to=b'self._meta.app_label/self._meta.model_name/trailer_image/', blank=True)),
                ('rating', django.contrib.postgres.fields.hstore.HStoreField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_last_modified', models.DateTimeField(auto_now=True)),
                ('enable', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('images', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.ImageField(upload_to=b'self._meta.app_label/self._meta.model_name/images/%Y/%m/%d/'), blank=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.CharField(max_length=100), blank=True)),
                ('related_items', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.IntegerField(), blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='option',
            field=models.ManyToManyField(to='options.Option'),
        ),
        migrations.AlterField(
            model_name='group',
            name='icon',
            field=models.ImageField(upload_to=b'self._meta.app_label/self._meta.model_name/icon/'),
        ),
        migrations.AddField(
            model_name='item',
            name='group',
            field=models.ForeignKey(to='materials.Group'),
        ),
        migrations.AddField(
            model_name='item',
            name='option_value',
            field=models.ManyToManyField(to='options.OptionValue'),
        ),
    ]
