from django.contrib import admin
from .models import Item, Attribute, AttributeValue, ItemAttributeRelationship
from django.db import models
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _


class ItemAttributeRelationshipInline(admin.TabularInline):
    model = ItemAttributeRelationship
    extra = 1

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'origin_title')
    inlines = (ItemAttributeRelationshipInline,)
    prepopulated_fields = {"slug": ("title", )}

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "cars":
    #         kwargs["queryset"] = Attribute.objects.filter()
    #     return super(ItemAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


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
