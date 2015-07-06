# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0051_auto_20150702_0806'),
        ('ex_user', '0002_auto_20150630_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='exuser',
            name='like_item',
            field=models.ManyToManyField(related_name='user_like', verbose_name='Like this', to='materials.Item'),
        ),
        migrations.AddField(
            model_name='exuser',
            name='not_like_item',
            field=models.ManyToManyField(related_name='user_not_like', verbose_name='Not like this', to='materials.Item'),
        ),
    ]
