from materials.models import Group, Item
from fs.core import ex_view

class IndexView(ex_view.ExtendView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        qs_item = Item.objects.filter(enable=1).select_related('main_group')
        context['items_popular'] = qs_item.order_by('-popular')[:8]
        context['items_comment'] = qs_item.all()[:4]
        context['items_new'] = qs_item.order_by('-date_create')[:20]
        qs_group = Group.objects.prefetch_related('groups')
        context['video'] = qs_group.get(slug='video')
        context['audio'] = qs_group.get(slug='audio')
        context['igry'] = qs_group.get(slug='igry')
        context['knigi'] = qs_group.get(slug='knigi')
        context['literatura'] = qs_group.get(slug='literatura')

        return context