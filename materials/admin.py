from django.contrib import admin
from .models import Group, Item, ItemAttribute, ItemAttributeValue, AttributeOption, ItemClass, Option
from django.db import models
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

class AttributeInline(admin.TabularInline):
    model = ItemAttributeValue

class ItemAttributeInline(admin.TabularInline):
    model = ItemAttribute
    extra = 2

class ItemAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'item_class', 'type')
    prepopulated_fields = {"code": ("name", )}

class ItemAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('item', 'attribute', 'value')

class ItemClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'requires_shipping', 'track_stock')
    inlines = [ItemAttributeInline]

class ItemAdmin(admin.ModelAdmin):
    list_display = ('date_create', 'title', 'enable')
    prepopulated_fields = {"slug": ("title", )}
    inlines = [AttributeInline]
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(
            verbose_name=_('grouped options'),
            is_stacked=False
        )},
    }

    def queryset(self, request):
        qs = super(ItemAdmin, self).queryset(request)
        return (
            qs
            .prefetch_related(
                'option_values',
                'option_values__option'))

class OptionAdmin(admin.ModelAdmin):
    pass

class AttributeOptionInline(admin.TabularInline):
    model = AttributeOption

class AttributeOptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'option_summary')
    inlines = [AttributeOptionInline, ]


admin.site.register(Group)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemClass, ItemClassAdmin)
admin.site.register(ItemAttribute, ItemAttributeAdmin)
admin.site.register(ItemAttributeValue, ItemAttributeValueAdmin)
admin.site.register(Option, OptionAdmin)