import goslate
from slugify import UniqueSlugify
from materials.models import Item, Group
import feedparser
from time import mktime
from datetime import datetime
from django.contrib.auth.models import User
from celery import task
import os
from haystack.management.commands import rebuild_index
slug = UniqueSlugify()
slug.to_lower = True


@task
def parser_premiere():
    user, __ = User.objects.get_or_create(username='admin')
    name_group = 'Video'
    group, __ = Group.objects.get_or_create(
        title=name_group, slug=slug(name_group))

    # gs = goslate.Goslate()
    url = os.environ.get('RSS_URL')
    items = feedparser.parse(url)

    for item in items.entries:
        title = item.title

        film, created = Item.objects.get_or_create(
            slug=slug(title),
            title=title,
            # origin_title=gs.translate(title, 'en'),
            creator=user,
            original_image=item.links[1].href,
            tags=[],
            main_group=group,
            description=item.summary,
            pub_date=datetime.fromtimestamp(mktime(item.published_parsed)))

    rebuild_index.Command().handle(interactive=False)
