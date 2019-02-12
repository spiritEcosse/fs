__author__ = 'igor'
from materials.models import Group


def context_data(request):
    return {'groups': Group.objects.filter(parent=None, enable=True).prefetch_related('groups')}