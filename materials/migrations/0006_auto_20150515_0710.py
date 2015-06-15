# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_remove_attributevalue_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name='Slug')),
                ('sort', models.IntegerField(null=True, verbose_name='Sort', blank=True)),
                ('parent', models.ForeignKey(related_name='groups', verbose_name='Parent', blank=True, to='materials.Group', null=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='groups',
            field=models.ManyToManyField(related_name='items', verbose_name='Group', to='materials.Group'),
        ),
    ]
