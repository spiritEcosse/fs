# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_item_structure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='icon',
            field=models.ImageField(upload_to=b'images/materials/%Y/%m/', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='group',
            field=models.ForeignKey(blank=True, to='materials.Group', null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(size=None, base_field=models.ImageField(upload_to=b'images/materials/%Y/%m/'), blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_class',
            field=models.ForeignKey(related_name='items', on_delete=django.db.models.deletion.PROTECT, blank=True, to='materials.ItemClass', help_text='Choose what type of item this is', null=True, verbose_name='Item type'),
        ),
        migrations.AlterField(
            model_name='item',
            name='main_image',
            field=models.ImageField(null=True, upload_to=b'images/materials/%Y/%m/', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='origin_title',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='trailer_image',
            field=models.ImageField(null=True, upload_to=b'images/materials/%Y/%m/', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='trailer_link',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='itemattributevalue',
            name='value_file',
            field=models.FileField(max_length=255, null=True, upload_to=b'images/materials/%Y/%m/', blank=True),
        ),
        migrations.AlterField(
            model_name='itemattributevalue',
            name='value_image',
            field=models.ImageField(max_length=255, null=True, upload_to=b'images/materials/%Y/%m/', blank=True),
        ),
    ]
