# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_auto_20150727_0856'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('img', models.ImageField(upload_to=b'images/ex_user/', verbose_name='Image', blank=True)),
                ('defer', models.ManyToManyField(related_name='users_defer', verbose_name='For the future', to='materials.Item')),
                ('like_item', models.ManyToManyField(related_name='user_like', verbose_name='Like this', to='materials.Item')),
                ('liked', models.ManyToManyField(related_name='users_liked', verbose_name='My Favorites', to='materials.Item')),
                ('not_like_item', models.ManyToManyField(related_name='user_not_like', verbose_name='Not like this', to='materials.Item')),
                ('user', models.OneToOneField(related_name='ex_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Extend user',
                'verbose_name_plural': 'Extends user',
            },
        ),
    ]
