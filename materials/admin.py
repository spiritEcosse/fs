from django.contrib import admin
from .models import Item, Attribute, AttributeValue, ItemAttributeRelationship
from django import forms
from django.db import models
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

class ItemAttributeRelationshipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemAttributeRelationshipForm, self).__init__(*args, **kwargs)

        if 'attribute' in self.initial:
            self.fields['attribute_values'].queryset = AttributeValue.objects.filter(attribute_id=self.initial['attribute'])

    class Meta:
        model = ItemAttributeRelationship
        fields = ['attribute', 'attribute_values']

class ItemAttributeRelationshipInline(admin.TabularInline):
    model = ItemAttributeRelationship
    extra = 0
    form = ItemAttributeRelationshipForm

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'origin_title')
    inlines = (ItemAttributeRelationshipInline,)
    prepopulated_fields = {"slug": ("title", )}

class AttributeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}

class AttributeValueAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}


admin.site.register(Item, ItemAdmin)
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
