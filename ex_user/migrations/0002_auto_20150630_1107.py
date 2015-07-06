# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0050_auto_20150630_1107'),
        ('ex_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exuser',
            name='defer',
            field=models.ManyToManyField(related_name='users_defer', verbose_name='For the future', to='materials.Item'),
        ),
        migrations.AddField(
            model_name='exuser',
            name='liked',
            field=models.ManyToManyField(related_name='users_liked', verbose_name='My Favorites', to='materials.Item'),
        ),
    ]
