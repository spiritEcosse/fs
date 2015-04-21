# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('icon', models.ImageField(height_field=20, width_field=20, upload_to=b'self._meta.app_label/self._meta.model_name/icon/')),
            ],
        ),
        migrations.CreateModel(
            name='OptionValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('option', models.ForeignKey(to='options.Option')),
            ],
        ),
    ]
