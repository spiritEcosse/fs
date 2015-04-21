from django.contrib import admin
from .models import Group, Item, ItemOption, ItemOptionValue
from django.db import models
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

class OptionInline(admin.TabularInline):
    model = ItemOptionValue

class ItemOptionInline(admin.TabularInline):
    model = ItemOption
    extra = 2

class ItemOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'type')
    prepopulated_fields = {"code": ("name", )}

class ItemOptionValueAdmin(admin.ModelAdmin):
    list_display = ('item', 'option', 'value')

# class ItemClassAdmin(admin.ModelAdmin):
#     list_display = ('name', 'requires_shipping', 'track_stock')
#     inlines = [ItemOptionInline]

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'origin_title')
    inlines = [OptionInline]
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

admin.site.register(Item, ItemAdmin)
admin.site.register(Group)
admin.site.register(ItemOption, ItemOptionAdmin)
admin.site.register(ItemOptionValue, ItemOptionValueAdmin)
