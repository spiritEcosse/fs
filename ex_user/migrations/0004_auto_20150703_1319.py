# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ex_user', '0003_auto_20150702_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exuser',
            name='img',
            field=models.ImageField(upload_to=b'images/ex_user/', verbose_name='Image', blank=True),
        ),
    ]
