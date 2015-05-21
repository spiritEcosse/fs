from materials.models import Group, Item, ItemAttributeRelationship
from fs.core import ex_view
from django.shortcuts import get_object_or_404

class DetailGroupView(ex_view.ExtendDetailView):
    model = Group

    def get_template_names(self):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])

        if group.parent:
            return super(DetailGroupView, self).get_template_names()
        return ['materials/main_group_detail.html']

class DetailItemView(ex_view.ExtendDetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super(DetailItemView, self).get_context_data(**kwargs)
        item = get_object_or_404(Item, slug=self.kwargs['slug'])
        item_attr_relate = ItemAttributeRelationship.objects.filter(item=item, attribute=item.attributes.all())
        attributes = []

        for attr in item_attr_relate:
            attributes.append((attr, attr.attribute_values.all()))

        context['attributes'] = attributes
        return context