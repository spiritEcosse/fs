__author__ = 'igor'
from materials.models import Group


class ExView(object):
    @staticmethod
    def extra_context_data():
        return {'groups': Group.objects.filter(parent=None, enable=1).prefetch_related('groups')}
