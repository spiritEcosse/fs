from haystack.generic_views import SearchView
from materials.models import Group, Item
from django.db.models import Count
from django.http import HttpResponse
from haystack.query import SearchQuerySet
import json
from haystack.inputs import AutoQuery
from django.template import defaultfilters
from django.core.urlresolvers import reverse_lazy


class MySearchView(SearchView):
    template_name = 'search/search.html'

    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        if 'group' in self.request.GET:
            queryset = SearchQuerySet().\
                filter(content=AutoQuery(self.request.GET['q']),
                       main_group_slug=self.request.GET.get('group'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MySearchView, self).get_context_data(**kwargs)

        if 'group' in self.request.GET:
            context['group_slug'] = self.request.GET.get('group')

        queryset = SearchQuerySet().filter(
            content=AutoQuery(self.request.GET['q']))
        list_item = [item.pk for item in queryset]
        context['groups_search'] = Group.objects.\
            filter(enable=1, items_main_group__pk__in=list_item).\
            annotate(count_items=Count('items_main_group')).distinct()
        return context


def autocomplete(request):
    sqs = SearchQuerySet().filter(content=AutoQuery(request.GET['q']))[:5]
    suggestions = [{
        'title':
        obj.title,
        'main_image':
        obj.main_image,
        'main_group_title':
        obj.main_group_title,
        'year_release':
        defaultfilters.date(obj.year_release, 'Y'),
        'href':
        reverse_lazy(
            'materials:detail_item',
            kwargs={
                'group_slug': obj.main_group_slug,
                'slug': obj.slug
            }).__str__(),
        'countries':
        defaultfilters.truncatechars(', '.join(obj.countries), 30),
        'genres':
        ', '.join(obj.genres)
    } for obj in sqs]
    the_data = json.dumps({'results': suggestions})
    return HttpResponse(the_data, content_type='application/json')
