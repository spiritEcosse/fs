__author__ = 'igor'
from django.views import generic
from django.views.generic.base import TemplateView
from materials.models import Group
from django.contrib.auth.forms import AuthenticationForm

class ExView(object):
    context = {}

    def context_data(self):
        self.context['groups'] = Group.objects.filter(parent=None, enable=1).prefetch_related('groups')
        self.context['form'] = AuthenticationForm()
        return self.context

class ExtendDetailView(generic.DetailView, ExView):
    def get_context_data(self, **kwargs):
        context = super(ExtendDetailView, self).get_context_data(**kwargs)
        context.update(self.context_data())
        return context

class ExtendView(TemplateView, ExView):
    def get_context_data(self, **kwargs):
        context = super(ExtendView, self).get_context_data(**kwargs)
        context.update(self.context_data())
        return context