# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name='Slug')),
                ('enable', models.BooleanField(default=True, verbose_name='Enable')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Attribute',
                'verbose_name_plural': 'Attributes',
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name='Slug')),
                ('attribute', models.ForeignKey(related_name='attribute_values', verbose_name='Attribute', to='materials.Attribute')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Attribute value',
                'verbose_name_plural': 'Attribute values',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('origin_title', models.CharField(max_length=200, verbose_name='Origin title', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name='Slug')),
                ('enable', models.BooleanField(default=True, verbose_name='Enable')),
                ('main_image', models.ImageField(upload_to=b'images/materials/%Y/%m/', null=True, verbose_name='Main Image', blank=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None, verbose_name='Tags', blank=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date_create'],
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='ItemAttributeRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.ForeignKey(to='materials.Attribute')),
                ('attribute_values', models.ManyToManyField(to='materials.AttributeValue')),
                ('item', models.ForeignKey(to='materials.Item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('attributes', models.ManyToManyField(related_name='item_classes', to='materials.Attribute')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Item class',
                'verbose_name_plural': 'Item classes',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='attributes',
            field=models.ManyToManyField(related_name='items', verbose_name='Attributes', through='materials.ItemAttributeRelationship', to='materials.Attribute'),
        ),
        migrations.AddField(
            model_name='item',
            name='item_class',
            field=models.ForeignKey(blank=True, to='materials.ItemClass', null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='recommend_item',
            field=models.ManyToManyField(related_name='recommend_item_rel_+', verbose_name='Recommended item', to='materials.Item', blank=True),
        ),
    ]
