# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0011_item_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemImages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'images/materials/%Y/%m/', verbose_name='Image item')),
                ('title', models.CharField(max_length=200, verbose_name='Title image', blank=True)),
                ('item', models.ForeignKey(related_name='images', to='materials.Item')),
            ],
        ),
    ]
