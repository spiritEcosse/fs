from materials.models import Group, Item, Attribute
from django.db.models import Q, F
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from materials.forms import CommentForm
from django.shortcuts import redirect


class AttributeDetailView(generic.DetailView):
    model = Attribute

    def get(self, request, *args, **kwargs):
        self.kwargs.get('slug', False)
        return super(AttributeDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AttributeDetailView, self).get_context_data(**kwargs)
        context.update(self.kwargs['extra_context'])
        group = get_object_or_404(Group, slug=self.kwargs['group_slug'])
        queryset_attribute_value = set()

        if self.request.GET.get('attribute_value', ()):
            queryset_attribute_value = set(self.request.GET.get('attribute_value').split('__'))

        link = self.build_link_on_exist_data('', 'attribute')
        link = self.build_link_on_exist_data(link, 'sort')
        context['attribute_values'] = []

        for value in self.object.attribute_values.all():
            value_set = queryset_attribute_value.copy()

            if value.slug not in queryset_attribute_value:
                value_set.add(value.slug)
            else:
                value.active = True
                value_set.discard(value.slug)

            link_value = link

            if value_set:
                link_value += '&' if link else '?'
                link_value += 'attribute_value=' + '__'.join(value_set)

            value.link = '%s%s' % \
                         (reverse('materials:detail_group', kwargs={'slug': group.slug_to_string()}), link_value)
            context['attribute_values'].append(value)

        link = self.build_link_on_exist_data(link, 'page')
        link = self.build_link_on_exist_data(link, 'attribute_value')
        context['back'] = '%s%s' % (reverse('materials:detail_group', kwargs={'slug': group.slug_to_string()}), link)
        context['group'] = group
        return context

    def build_link_on_exist_data(self, link, param):
        if self.request.GET.get(param, ''):
            link += '&' if link else '?'
            link += '%s=%s' % (param, self.request.GET.get(param))
        return link


class DetailGroupView(generic.DetailView):
    model = Group

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('slug', False):
            self.kwargs['slug'] = self.kwargs['slug'].split('/').pop()
        return super(DetailGroupView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailGroupView, self).get_context_data(**kwargs)
        context.update(self.kwargs['extra_context'])
        queryset = Item.objects.filter(Q(main_group=self.object) | Q(groups=self.object), enable=1).\
            select_related('main_group')
        context['items_popular'] = queryset.order_by('-popular')[:8]
        context['breadcrumbs'] = self.object.get_tree_group([])
        page = self.request.GET.get('page')
        queryset_attribute = set()
        queryset_attribute_value = self.request.GET.get('attribute_value', '')

        if self.request.GET.get('attribute', ()):
            queryset_attribute = set(self.request.GET.get('attribute').split('__'))
            queryset = queryset.filter(item_attr__attribute__slug__in=queryset_attribute)

        if queryset_attribute_value:
            attribute_value = set(self.request.GET.get('attribute_value').split('__'))
            queryset = queryset.filter(item_attr__attribute_values__slug__in=attribute_value)

        link = self.build_link_on_exist_data('', 'page')
        link = self.build_link_on_exist_data(link, 'sort')
        link = self.build_link_on_exist_data(link, 'attribute_value')

        for attribute in self.object.attributes.all():
            for children in attribute.children.all():
                attr_set = queryset_attribute.copy()

                if not children.attribute_values.exists():
                    if children.slug not in queryset_attribute:
                        attr_set.add(children.slug)
                    else:
                        children.active = True
                        attr_set.discard(children.slug)
                attribute_link = link

                if attr_set:
                    attribute_link += '&' if attribute_link else '?'
                    attribute_link += 'attribute=' + '__'.join(attr_set)

                if queryset_attribute_value:
                    children_attribute_value = {value.slug for value in children.attribute_values.all()}
                    attribute_value_get = set(self.request.GET.get('attribute_value').split('__'))

                    if children_attribute_value.intersection(attribute_value_get):
                        children.active = True
                children.link = self.object.get_absolute_url() + attribute_link

                if children.attribute_values.exists():
                    children.link = '%s%s' % (reverse('materials:attribute', kwargs={
                        'slug': children.slug,
                        'group_slug': self.object.slug
                    }), attribute_link)

        link = self.build_link_on_exist_data('', 'page')
        link_sort = self.build_link_on_exist_data(link, 'attribute')
        link_sort = self.build_link_on_exist_data(link_sort, 'attribute_value')

        keys = {'date_create': _('date added'),
                'year_release': _('year release'),
                'popular': _('popular'),
                'sort': _('in trend'),
                'like': _('by rating')}
        context['link_sort'] = [(value, self.build_link(link_sort, 'sort', key)) for key, value in keys.items()]

        link = self.build_link_on_exist_data('', 'sort')
        link = self.build_link_on_exist_data(link, 'attribute')
        link = self.build_link_on_exist_data(link, 'attribute_value')

        context['sort'] = keys.get(self.request.GET.get('sort'), 'date_create')

        if self.request.GET.get('sort') == 'like':
            queryset = queryset.annotate(diff_like=F('like')-F('not_like')).order_by('-diff_like')
        elif self.request.GET.get('sort', ''):
            queryset = queryset.order_by('-%s' % self.request.GET.get('sort'))
        else:
            queryset = queryset.order_by('sort')

        items = queryset
        paginator = Paginator(items, 24)
        paginator.link = link

        try:
            context['items'] = paginator.page(page)
        except PageNotAnInteger:
            context['items'] = paginator.page(1)
        except EmptyPage:
            context['items'] = paginator.page(paginator.num_pages)

        return context

    def build_link(self, link, param, value):
        link += '&' if link else '?'
        link += '%s=%s' % (param, value)
        return link

    def build_link_on_exist_data(self, link, param):
        if self.request.GET.get(param, ''):
            link += '&' if link else '?'
            link += '%s=%s' % (param, self.request.GET.get(param))
        return link

    def get_queryset(self):
        qs = super(DetailGroupView, self).get_queryset()

        return qs.\
            filter(enable=1).prefetch_related('attributes', 'attributes__children')

    def get_template_names(self):
        if self.object.parent:
            return super(DetailGroupView, self).get_template_names()
        return ['materials/main_group_detail.html']


class ExtendContextDataItem(object):
    def __init__(self, view):
        self.view = view

    def get_context_data(self):
        return {
            'recommend_item': self.view.object.recommend_item.filter(enable=1)[:8],
            'count_comments': self.view.object.comments.count(),
            'user_like': self.view.object.users_liked.filter(user=self.view.request.user.id),
            'user_defer': self.view.object.users_defer.filter(user=self.view.request.user.id),
        }


class CommentHandler(SingleObjectMixin, FormView):
    model = Item
    template_name = 'materials/item_detail.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(reverse('login'))
        self.object = self.get_object()

        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.object_id = self.object.pk
            comment.content_type = ContentType.objects.get_for_model(self.model)
            comment.user = request.user
            comment.save()
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CommentHandler, self).get_context_data(**kwargs)
        context.update(self.kwargs['extra_context'])
        context['form_comment'] = self.get_form()
        ex_context_data = ExtendContextDataItem(self)
        context.update(ex_context_data.get_context_data())
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()


class DetailItemView(FormMixin, generic.DetailView):
    model = Item

    def get_queryset(self):
        qs = super(DetailItemView, self).get_queryset()
        return qs\
            .filter(enable=1)\
            .select_related('creator', 'main_group')\
            .prefetch_related('main_group__groups', 'comments', 'comments__user', 'recommend_item', 'images',
                              'item_attr__attribute', 'item_attr__attribute_values')

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)

        if slug is not None:
            self.kwargs['slug'] = self.kwargs['slug'].split('/').pop()
        return super(DetailItemView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.model.objects.filter(pk=self.object.pk).update(popular=F('popular') + 1)

        context = super(DetailItemView, self).get_context_data(**kwargs)
        context.update(self.kwargs['extra_context'])
        context['form_comment'] = CommentForm
        ex_context_data = ExtendContextDataItem(self)
        context.update(ex_context_data.get_context_data())
        return context


class ItemDetail(View):
    def get(self, request, *args, **kwargs):
        view = DetailItemView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentHandler.as_view()
        return view(request, *args, **kwargs)


@csrf_exempt
@require_POST
def put_item(request, **kwargs):
    pk = request.POST.get('item_pk')
    item = get_object_or_404(Item, pk=pk)
    data = {}

    if request.POST.get('type_btn') == '0':
        data['text'] = unicode(_('Favoured'))
        request.user.ex_user.liked.add(item)
    elif request.POST.get('type_btn') == '1':
        data['text'] = unicode(_('For the future'))
        request.user.ex_user.defer.add(item)
    else:
        raise Exception('type_btn is not valid')

    data['success'] = True
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json; charset=utf8")


@csrf_exempt
@require_POST
def del_item(request, **kwargs):
    pk = request.POST.get('item_pk')
    item = get_object_or_404(Item, pk=pk)
    data = {}

    if request.POST.get('type_btn') == '0':
        data['text'] = unicode(_('Add to favorites'))
        request.user.ex_user.liked.remove(item)
    elif request.POST.get('type_btn') == '1':
        data['text'] = unicode(_('Add for the future'))
        request.user.ex_user.defer.remove(item)
    else:
        raise Exception('type_btn is not valid')

    data['success'] = True
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json; charset=utf8")


@csrf_exempt
@require_POST
def vote(request, **kwargs):
    pk = request.POST.get('item_pk')
    item = get_object_or_404(Item, pk=pk)
    data = {}

    if request.POST.get('type_btn') == '0':
        item.not_like += 1
        item.save()
        request.user.ex_user.not_like_item.add(item)
        request.user.ex_user.save()
        data['number'] = item.not_like
    elif request.POST.get('type_btn') == '1':
        item.like += 1
        item.save()
        request.user.ex_user.like_item.add(item)
        request.user.ex_user.save()
        data['number'] = item.like
    else:
        raise Exception('type_btn is not valid')

    data['success'] = True
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json; charset=utf8")


@csrf_exempt
@require_POST
def cancel_vote(request, **kwargs):
    pk = request.POST.get('item_pk')
    item = get_object_or_404(Item, pk=pk)
    data = {}

    if request.POST.get('type_btn') == '0':
        item.not_like -= 1
        item.save()
        data['number'] = item.not_like
        request.user.ex_user.not_like_item.remove(item)
        request.user.ex_user.save()
    elif request.POST.get('type_btn') == '1':
        item.like -= 1
        item.save()
        data['number'] = item.like
        request.user.ex_user.like_item.remove(item)
        request.user.ex_user.save()
    else:
        raise Exception('type_btn is not valid')

    data['success'] = True
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json; charset=utf8')