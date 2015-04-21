# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import fs.models.fields.autoslugfield
import django.contrib.postgres.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('option', models.CharField(max_length=255, verbose_name='Option')),
            ],
            options={
                'verbose_name': 'Attribute option',
                'verbose_name_plural': 'Attribute options',
            },
        ),
        migrations.CreateModel(
            name='AttributeOptionGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Attribute option group',
                'verbose_name_plural': 'Attribute option groups',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('icon', models.ImageField(upload_to=b'images/products/%Y/%m/', blank=True)),
                ('enable', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_last_modified', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, to='materials.Group', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('origin_title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('main_image', models.ImageField(upload_to=b'images/products/%Y/%m/')),
                ('trailer_link', models.URLField(blank=True)),
                ('trailer_image', models.ImageField(upload_to=b'images/products/%Y/%m/', blank=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_last_modified', models.DateTimeField(auto_now=True)),
                ('enable', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('images', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.ImageField(upload_to=b'images/products/%Y/%m/'), blank=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.CharField(max_length=100), blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemAttribute',
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
            name='ItemAttributeValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value_text', models.TextField(null=True, verbose_name='Text', blank=True)),
                ('value_integer', models.IntegerField(null=True, verbose_name='Integer', blank=True)),
                ('value_boolean', models.NullBooleanField(verbose_name='Boolean')),
                ('value_float', models.FloatField(null=True, verbose_name='Float', blank=True)),
                ('value_richtext', models.TextField(null=True, verbose_name='Richtext', blank=True)),
                ('value_date', models.DateField(null=True, verbose_name='Date', blank=True)),
                ('value_file', models.FileField(max_length=255, null=True, upload_to=b'images/products/%Y/%m/', blank=True)),
                ('value_image', models.ImageField(max_length=255, null=True, upload_to=b'images/products/%Y/%m/', blank=True)),
                ('entity_object_id', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('attribute', models.ForeignKey(verbose_name='Attribute', to='materials.ItemAttribute')),
                ('entity_content_type', models.ForeignKey(blank=True, editable=False, to='contenttypes.ContentType', null=True)),
                ('item', models.ForeignKey(related_name='attribute_values', verbose_name='Item', to='materials.Item')),
                ('value_option', models.ForeignKey(verbose_name='Value option', blank=True, to='materials.AttributeOption', null=True)),
            ],
            options={
                'verbose_name': 'Item attribute value',
                'verbose_name_plural': 'Item attribute values',
            },
        ),
        migrations.CreateModel(
            name='ItemClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', fs.models.fields.autoslugfield.AutoSlugField(populate_from=b'name', editable=False, max_length=128, blank=True, unique=True, verbose_name='Slug')),
                ('requires_shipping', models.BooleanField(default=True, verbose_name='Requires shipping?')),
                ('track_stock', models.BooleanField(default=True, verbose_name='Track stock levels?')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Item class',
                'verbose_name_plural': 'Item classes',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('code', fs.models.fields.autoslugfield.AutoSlugField(populate_from=b'name', editable=False, max_length=128, blank=True, unique=True, verbose_name='Code')),
                ('type', models.CharField(default=b'Required', max_length=128, verbose_name='Status', choices=[(b'Required', 'Required - a value for this option must be specified'), (b'Optional', 'Optional - a value for this option can be omitted')])),
            ],
            options={
                'verbose_name': 'Option',
                'verbose_name_plural': 'Options',
            },
        ),
        migrations.AddField(
            model_name='itemclass',
            name='options',
            field=models.ManyToManyField(to='materials.Option', verbose_name='Options', blank=True),
        ),
        migrations.AddField(
            model_name='itemattribute',
            name='item_class',
            field=models.ForeignKey(related_name='attributes', verbose_name='Item type', blank=True, to='materials.ItemClass', null=True),
        ),
        migrations.AddField(
            model_name='itemattribute',
            name='option_group',
            field=models.ForeignKey(blank=True, to='materials.AttributeOptionGroup', help_text='Select an option group if using type "Option"', null=True, verbose_name='Option Group'),
        ),
        migrations.AddField(
            model_name='item',
            name='attributes',
            field=models.ManyToManyField(help_text='A item attribute is something that this item may have, such as a size, as specified by its class', to='materials.ItemAttribute', verbose_name='Attributes', through='materials.ItemAttributeValue'),
        ),
        migrations.AddField(
            model_name='item',
            name='group',
            field=models.ForeignKey(to='materials.Group'),
        ),
        migrations.AddField(
            model_name='item',
            name='item_class',
            field=models.ForeignKey(related_name='items', on_delete=django.db.models.deletion.PROTECT, verbose_name='Item type', to='materials.ItemClass', help_text='Choose what type of item this is', null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='item_options',
            field=models.ManyToManyField(help_text="Options are values that can be associated with a item when it is added to a customer's basket.  This could be something like a personalised message to be printed on a T-shirt.", to='materials.Option', verbose_name='Item options', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='materials.Item', help_text="Only choose a parent item if you're creating a child item.  For example if this is a size 4 of a particular t-shirt.  Leave blank if this is a stand-alone item (i.e. there is only one version of this item).", null=True, verbose_name='Parent item'),
        ),
        migrations.AddField(
            model_name='item',
            name='related_items',
            field=models.ManyToManyField(related_name='related_items_rel_+', to='materials.Item', blank=True),
        ),
        migrations.AddField(
            model_name='attributeoption',
            name='group',
            field=models.ForeignKey(related_name='options', verbose_name='Group', to='materials.AttributeOptionGroup'),
        ),
        migrations.AlterUniqueTogether(
            name='itemattributevalue',
            unique_together=set([('attribute', 'item')]),
        ),
    ]
