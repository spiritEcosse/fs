from django.contrib import admin
from .models import Item, ItemClass, Attribute, AttributeValue, ItemAttributeRelationship
from django import forms
from django.db.models import Q
from django.db import models
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from django.forms.models import BaseInlineFormSet, BaseModelFormSet
from django.core.exceptions import ValidationError

class ItemAttributeRelationshipForm(BaseInlineFormSet):
    class Meta:
        model = ItemAttributeRelationship
        fields = ['attribute', 'attribute_values']

    def clean(self):
        super(ItemAttributeRelationshipForm, self).clean()

        if self.instance.item_class:
            attr_form = set()

            for form in self.forms:
                if 'attribute' in form.cleaned_data:
                    attr_form.add(form.cleaned_data['attribute'])

            attr_class = set(self.instance.item_class.attributes.all())
            diff_attr = attr_class.difference(attr_form)

            if diff_attr:
                validate_error = []

                for attr in diff_attr:
                    validate_error.append(_('%s attribute cannot be blank') % attr)

                if validate_error:
                    raise ValidationError(validate_error)

class ItemAttributeRelationshipInline(admin.TabularInline):
    model = ItemAttributeRelationship
    extra = 0
    formset = ItemAttributeRelationshipForm

    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super(ItemAttributeRelationshipInline, self).get_formset(request, obj=None, **kwargs)
    #     raise Exception(formset)

    # def get_queryset(self, request):
    #     raise Exception(self)
        # queryset = super(AttributeInline, self).get_queryset(request)
        # queryset = Attribute.objects.none()
        # queryset = Attribute.objects.filter(Q(item_classes=1) | Q(items=5))
        # queryset = Attribute.objects.filter(Q(item=5) | Q(attribute__item_classes=1))
        # raise Exception(queryset)
            # attribute.item_classes.filter(pk=Item.objects.get(pk=5).item_class)
        # raise Exception(queryset)
        # return queryset

    # def get_formset(self, request, obj=None, **kwargs):
    #     super(ItemAttributeRelationshipInline, self).get_formset(request, obj=None, **kwargs)
        # raise Exception(self.formset.__dict__)
    #     return formset

        # raise Exception(self.get_queryset(request))
        # raise Exception(dir(self))

        #     raise Exception(dir(self))
        #
        #     raise Exception(dir(self))

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'origin_title', 'attribute_summary', 'date_create', 'item_class', 'enable')
    inlines = [ItemAttributeRelationshipInline]
    prepopulated_fields = {"slug": ("title", )}

    def get_queryset(self, request):
        qs = super(ItemAdmin, self).get_queryset(request)
        return qs\
            .select_related('item_class')\
            .prefetch_related('attributes', 'attributes__attribute_values', 'recommend_item')

class AttributeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}

class AttributeValueAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemClass)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeValue, AttributeValueAdmin)


# class AttributeInline(admin.TabularInline):
#     model = ItemAttributeValue
#
# class ItemAttributeInline(admin.TabularInline):
#     model = ItemAttribute
#     extra = 2
#
# class ItemAttributeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'code', 'item_class', 'type')
#     prepopulated_fields = {"code": ("name", )}
#
# class ItemAttributeValueAdmin(admin.ModelAdmin):
#     list_display = ('item', 'attribute', 'value')
#
# class ItemClassAdmin(admin.ModelAdmin):
#     list_display = ('name', 'requires_shipping', 'track_stock')
#     inlines = [ItemAttributeInline]
#
# class ItemAdmin(admin.ModelAdmin):
#     list_display = ('get_title', 'get_item_class', 'structure', 'attribute_summary', 'date_create', 'enable')
#     prepopulated_fields = {"slug": ("title", )}
#     inlines = [AttributeInline]
#     formfield_overrides = {
#         models.ManyToManyField: {'widget': FilteredSelectMultiple(
#             verbose_name=_('grouped options'),
#             is_stacked=False
#         )},
#     }
#
#     def queryset(self, request):
#         qs = super(ItemAdmin, self).queryset(request)
#         return (
#             qs
#             .prefetch_related(
#                 'option_values',
#                 'option_values__option'))
#
# class OptionAdmin(admin.ModelAdmin):
#     pass
#
# class AttributeOptionInline(admin.TabularInline):
#     model = AttributeOption
#
# class AttributeOptionGroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'option_summary')
#     inlines = [AttributeOptionInline, ]
#
#
# admin.site.register(Group)
# admin.site.register(Item, ItemAdmin)
# admin.site.register(ItemClass, ItemClassAdmin)
# admin.site.register(ItemAttribute, ItemAttributeAdmin)
# admin.site.register(ItemAttributeValue, ItemAttributeValueAdmin)
# admin.site.register(Option, OptionAdmin)
