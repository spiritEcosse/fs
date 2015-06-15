# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('materials', '0019_remove_item_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='creator',
            field=models.ForeignKey(related_name='items', default=1, editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
