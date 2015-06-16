# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('img', models.ImageField(upload_to=b'images/ex_user/', verbose_name='Image')),
                ('user', models.OneToOneField(related_name='ex_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Extend user',
                'verbose_name_plural': 'Extends user',
            },
        ),
    ]
