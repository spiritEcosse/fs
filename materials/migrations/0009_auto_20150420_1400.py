# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('materials', '0008_auto_20150417_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('code', models.SlugField(max_length=128, verbose_name='Code', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z\\-_][0-9a-zA-Z\\-_]*$', message="Code can only contain the letters a-z, A-Z, digits, minus and underscores, and can't start with a digit")])),
                ('type', models.CharField(default=b'text', max_length=20, verbose_name='Type', choices=[(b'text', 'Text'), (b'integer', 'Integer'), (b'boolean', 'True / False'), (b'float', 'Float'), (b'richtext', 'Rich Text'), (b'date', 'Date'), (b'option', 'Option'), (b'entity', 'Entity'), (b'file', 'File'), (b'image', 'Image')])),
                ('required', models.BooleanField(default=False, verbose_name='Required')),
            ],
            options={
                'ordering': ['code'],
                'verbose_name': 'Item option',
                'verbose_name_plural': 'Item options',
            },
        ),
        migrations.CreateModel(
            name='ItemOptionValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value_text', models.TextField(null=True, verbose_name='Text', blank=True)),
                ('value_integer', models.IntegerField(null=True, verbose_name='Integer', blank=True)),
                ('value_boolean', models.NullBooleanField(verbose_name='Boolean')),
                ('value_float', models.FloatField(null=True, verbose_name='Float', blank=True)),
                ('value_richtext', models.TextField(null=True, verbose_name='Richtext', blank=True)),
                ('value_date', models.DateField(null=True, verbose_name='Date', blank=True)),
                ('value_file', models.FileField(max_length=255, null=True, upload_to=b'self._meta.app_label', blank=True)),
                ('value_image', models.ImageField(max_length=255, null=True, upload_to=b'self._meta.app_label', blank=True)),
                ('entity_object_id', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('entity_content_type', models.ForeignKey(blank=True, editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'verbose_name': 'Item option value',
                'verbose_name_plural': 'Item option values',
            },
        ),
        migrations.RemoveField(
            model_name='item',
            name='name',
        ),
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='', max_length=255, verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='title',
            field=models.CharField(default='', max_length=100, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='icon',
            field=models.ImageField(upload_to=b'self._meta.app_label/icon/', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(size=None, base_field=models.ImageField(upload_to=b'/item/images/%Y/%m/%d/'), blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='main_image',
            field=models.ImageField(upload_to=b'/item/main_image/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='item',
            name='rating',
            field=models.FloatField(verbose_name='Rating', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='trailer_image',
            field=models.ImageField(upload_to=b'/item/trailer_image/', blank=True),
        ),
        migrations.AddField(
            model_name='itemoptionvalue',
            name='item',
            field=models.ForeignKey(related_name='option_values', verbose_name='Item', to='materials.Item'),
        ),
        migrations.AddField(
            model_name='itemoptionvalue',
            name='option',
            field=models.ForeignKey(verbose_name='Option', to='materials.ItemOption'),
        ),
        migrations.AddField(
            model_name='item',
            name='attributes',
            field=models.ManyToManyField(help_text='A item option is something that this item may have, such as a size, as specified by its class', to='materials.ItemOption', verbose_name='Options', through='materials.ItemOptionValue'),
        ),
        migrations.AlterUniqueTogether(
            name='itemoptionvalue',
            unique_together=set([('option', 'item')]),
        ),
    ]
