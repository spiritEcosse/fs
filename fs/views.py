from materials.models import Group, Item
from fs.core import ex_view

class IndexView(ex_view.ExtendView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['items_popular'] = Item.objects.order_by('-popular')[:8]
        context['items_comment'] = Item.objects.all()[:4]
        context['request'] = self.request
        context['items_new'] = Item.objects.order_by('-date_create')[:20]
        return context