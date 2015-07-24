# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name='Slug')),
                ('enable', models.BooleanField(default=True, verbose_name='Enable')),
                ('on_item', models.BooleanField(default=False, verbose_name='Show on item')),
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
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name='Slug')),
                ('sort', models.IntegerField(default=0, verbose_name='Sort', blank=True)),
                ('enable', models.BooleanField(default=True, verbose_name='Enable')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
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
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('origin_title', models.CharField(max_length=200, verbose_name='Origin title', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name='Slug')),
                ('main_image', models.ImageField(upload_to=b'images/materials/%Y/%m/', verbose_name='Main Image')),
                ('description', models.TextField(verbose_name='Description')),
                ('year_release', models.DateField(default=datetime.datetime(2015, 7, 24, 10, 51, 1, 293591, tzinfo=utc), verbose_name='Year release')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_last_modified', models.DateTimeField(auto_now=True)),
                ('popular', models.BigIntegerField(default=0, verbose_name='Popular', editable=False, blank=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None, verbose_name='Tags', blank=True)),
                ('like', models.BigIntegerField(default=0, verbose_name='Like')),
                ('not_like', models.BigIntegerField(default=0, verbose_name='Not like')),
                ('sort', models.IntegerField(default=0, verbose_name='Sort', blank=True)),
                ('enable', models.BooleanField(default=True, verbose_name='Enable')),
                ('video', models.TextField(verbose_name=b'Video')),
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
                ('attribute', models.ForeignKey(related_name='item_attributes', to='materials.Attribute')),
                ('attribute_values', models.ManyToManyField(to='materials.AttributeValue', blank=True)),
                ('item', models.ForeignKey(related_name='item_attr', to='materials.Item')),
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
        migrations.CreateModel(
            name='ItemImages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'images/materials/%Y/%m/', verbose_name='Image item')),
                ('title', models.CharField(max_length=200, verbose_name='Title image', blank=True)),
                ('item', models.ForeignKey(related_name='images', to='materials.Item')),
            ],
        ),
        migrations.CreateModel(
            name='ProxyCountry',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('cities.country',),
        ),
        migrations.AddField(
            model_name='item',
            name='attributes',
            field=models.ManyToManyField(related_name='items', verbose_name='Attributes', through='materials.ItemAttributeRelationship', to='materials.Attribute'),
        ),
        migrations.AddField(
            model_name='item',
            name='countries',
            field=models.ManyToManyField(to='materials.ProxyCountry', verbose_name='Countries production'),
        ),
        migrations.AddField(
            model_name='item',
            name='creator',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='genres',
            field=models.ManyToManyField(related_name='items', verbose_name='Genre', to='materials.Genre', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='groups',
            field=models.ManyToManyField(related_name='items', verbose_name='Group', to='materials.Group', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='item_class',
            field=models.ForeignKey(blank=True, to='materials.ItemClass', null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='main_group',
            field=models.ForeignKey(related_name='items_main_group', verbose_name='Main Group', to='materials.Group'),
        ),
        migrations.AddField(
            model_name='item',
            name='recommend_item',
            field=models.ManyToManyField(related_name='recommend_item_rel_+', verbose_name='Recommended item', to='materials.Item', blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='icon',
            field=models.ForeignKey(blank=True, to='materials.Icon', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(related_name='groups', verbose_name='Parent', blank=True, to='materials.Group', null=True),
        ),
        migrations.AddField(
            model_name='attribute',
            name='groups',
            field=models.ManyToManyField(related_name='attributes', verbose_name='Group', to='materials.Group', blank=True),
        ),
        migrations.AddField(
            model_name='attribute',
            name='icon',
            field=models.ForeignKey(blank=True, to='materials.Icon', null=True),
        ),
        migrations.AddField(
            model_name='attribute',
            name='parent',
            field=models.ForeignKey(related_name='children', verbose_name='Parent', blank=True, to='materials.Attribute', null=True),
        ),
    ]
