# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0026_auto_20150604_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='groups',
            field=models.ManyToManyField(related_name='groups_rel_+', verbose_name='Group attributes', to='materials.Attribute', blank=True),
        ),
        migrations.AddField(
            model_name='attribute',
            name='image',
            field=models.ImageField(upload_to=b'images/materials/attribute/image/', verbose_name='Icon', blank=True),
        ),
        migrations.AddField(
            model_name='attribute',
            name='on_item',
            field=models.BooleanField(default=False, verbose_name='Show on item'),
        ),
    ]
