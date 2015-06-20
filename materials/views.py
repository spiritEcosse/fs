from materials.models import Group, Item
from django.db.models import Q, F
from comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm, HiddenInput
from django.views.generic import View
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden
from django.views.generic.edit import FormMixin
from django import forms
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class DetailGroupView(generic.DetailView):
    model = Group

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)

        if slug is not None:
            self.kwargs['slug'] = self.kwargs['slug'].split('/').pop()
        return super(DetailGroupView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailGroupView, self).get_context_data(**kwargs)
        context.update(self.kwargs['extra_context'])
        queryset = Item.objects.filter(Q(main_group=self.object) | Q(groups=self.object), enable=1).\
            select_related('main_group')
        context['items_popular'] = queryset.order_by('-popular')[:8]
        items = queryset.order_by()
        context['breadcrumbs'] = self.object.get_tree_group([])

        paginator = Paginator(items, 24)
        page = self.request.GET.get('page')

        try:
            context['items'] = paginator.page(page)
        except PageNotAnInteger:
            context['items'] = paginator.page(1)
        except EmptyPage:
            context['items'] = paginator.page(paginator.num_pages)

        return context

    def get_queryset(self):
        qs = super(DetailGroupView, self).get_queryset()

        return qs.\
            filter(enable=1)

    def get_template_names(self):
        if self.object.parent:
            return super(DetailGroupView, self).get_template_names()
        return ['materials/main_group_detail.html']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'text', 'object_id', 'content_type', 'like_object']
        widgets = {
            'object_id': HiddenInput(),
            'content_type': HiddenInput(),
            'user': HiddenInput(),
            'text': forms.Textarea(attrs={'placeholder': _('You comment')})
        }
        labels = {
            'text': '',
        }
        error_messages = {
            'text': {
                'require': _("This field required."),
            },
        }


class ExtendContextDataItem(object):
    def __init__(self, view):
        self.view = view

    def get_context_data(self):
        return {
            'recommend_item': self.view.object.recommend_item.filter(enable=1)[:8],
            'count_comments': self.view.object.comments.count(),
        }


class CommentHandler(SingleObjectMixin, FormView):
    model = Item
    template_name = 'materials/item_detail.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()

        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
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
        context['form_comment'] = CommentForm(initial={
            'object_id': self.object.pk,
            'content_type': ContentType.objects.get_for_model(self.model),
        })

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
