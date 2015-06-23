from materials.models import Group, Item
from fs.core import ex_view
from django.db.models import Count
from random import shuffle
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        qs_item = Item.objects.filter(enable=1).select_related('main_group')
        context['items_popular'] = qs_item.order_by('-popular')[:8]
        c_type = ContentType.objects.get(app_label="materials", model="item")
        context['items_comment'] = qs_item.prefetch_related('comments', 'comments__user').\
        annotate(count_comment=Count('comments')).filter(count_comment__gte=2, comments__content_type=c_type)[:16]
        context['items_new'] = qs_item.select_related('creator', 'main_group').order_by('-date_create')[:20]

        qs_group = Group.objects.prefetch_related('groups')
        context['video'] = qs_group.get(slug='video')
        context['audio'] = qs_group.get(slug='audio')
        context['igry'] = qs_group.get(slug='igry')
        context['knigi'] = qs_group.get(slug='knigi')
        context['literatura'] = qs_group.get(slug='literatura')
        return context
