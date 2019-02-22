import goslate
from slugify import UniqueSlugify
from materials.models import Item, Group
import feedparser
from time import mktime
from datetime import datetime
from django.contrib.auth.models import User
from celery import task

slug = UniqueSlugify()
slug.to_lower = True


@task
def parser_premiere():
    user = User.objects.create(username='admin')
    name_group = 'Video'
    group = Group.objects.create(title=name_group, slug=slug(name_group))

    # gs = goslate.Goslate()
    url = 'http://st.kp.yandex.net/rss/premiere.rss'
    items = feedparser.parse(url)

    for item in items.entries:
        title = item.title
        film, created = Item.objects.get_or_create(
            slug=slug(title),
            title=title,
            creator=user,
            tags=[],
            main_group=group,
            description=item.description,
            pub_date=datetime.fromtimestamp(mktime(item.published_parsed)))
        # film.title_uk = gs.translate(title, 'uk')
        # film.title_en = gs.translate(title, 'en')
