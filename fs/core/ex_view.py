__author__ = 'igor'
from django.views import generic
from django.views.generic.base import TemplateView
from materials.models import Group

def get_group_obj():
    return Group.objects.filter(parent=None).prefetch_related('groups')

class ExtendDetailView(generic.DetailView):
    def get_context_data(self, **kwargs):
        context = super(ExtendDetailView, self).get_context_data(**kwargs)
        context['groups'] = get_group_obj()
        return context

class ExtendView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(ExtendView, self).get_context_data(**kwargs)
        context['groups'] = get_group_obj()
        return context