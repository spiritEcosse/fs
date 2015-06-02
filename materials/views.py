from materials.models import Group, Item
from fs.core import ex_view
from django.db.models import Q, F

class DetailGroupView(ex_view.ExtendDetailView):
    model = Group

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)

        if slug is not None:
            self.kwargs['slug'] = self.kwargs['slug'].split('/').pop()
        return super(DetailGroupView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailGroupView, self).get_context_data(**kwargs)
        queryset = Item.objects.filter(Q(main_group=self.object) | Q(groups=self.object), enable=1).\
            select_related('main_group')
        context['items_popular'] = queryset.order_by('-popular')[:8]
        context['items'] = queryset
        context['breadcrumbs'] = self.object.get_tree_group([])
        return context

    def get_queryset(self):
        qs = super(DetailGroupView, self).get_queryset()

        return qs.\
            filter(enable=1)

    def get_template_names(self):
        if self.object.parent:
            return super(DetailGroupView, self).get_template_names()
        return ['materials/main_group_detail.html']

class DetailItemView(ex_view.ExtendDetailView):
    model = Item

    def get_queryset(self):
        qs = super(DetailItemView, self).get_queryset()
        return qs\
            .filter(enable=1)\
            .prefetch_related('attributes', 'attributes__attribute_values', 'recommend_item', 'images')

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)

        if slug is not None:
            self.kwargs['slug'] = self.kwargs['slug'].split('/').pop()
        return super(DetailItemView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        Item.objects.filter(pk=self.object.pk).update(popular=F('popular') + 1)
        context = super(DetailItemView, self).get_context_data(**kwargs)
        context['recommend_item'] = self.object.recommend_item.filter(enable=1)[:8]
        attributes = []

        for attr in self.object.item_attr.all():
            attributes.append((attr.attribute, attr.attribute_values.all()[:3], attr.attribute_values.all()[3:]))

        context['attributes'] = attributes
        return context