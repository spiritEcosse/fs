from django.contrib import admin
from .models import Item, ItemClass, Attribute, AttributeValue, ItemAttributeRelationship, Group, ItemImages
from django.utils.translation import ugettext_lazy as _
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db.models import When, Case

def change_status(modeladmin, request, queryset):
    queryset.update(
        enable=Case(
            When(enable=True, then=False),
            When(enable=False, then=True)
        )
    )
change_status.short_description = _("Change status")

class ItemAttributeRelationshipForm(BaseInlineFormSet):
    class Meta:
        model = ItemAttributeRelationship
        fields = ['attribute', 'attribute_values']

    def __init__(self, *args, **kwargs):
        super(ItemAttributeRelationshipForm, self).__init__(*args, **kwargs)

        # raise Exception(self.forms)
        # self.initial_extra = [{'attribute': 1, 'attribute_values': [2, 4, 6]}]

        # if getattr(self.initial, 'attribute', None):
        #     raise Exception(self.initial['attribute'])
        #
        #     self.fields['attribute_values'].queryset = AttributeValue.objects.\
        #         filter(attribute_id=self.initial['attribute'])

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
    extra = 5
    formset = ItemAttributeRelationshipForm

class ItemImagesInline(admin.TabularInline):
    model = ItemImages

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'main_group', 'origin_title', 'creator', 'attribute_summary', 'date_create', 'item_class', 'enable')
    inlines = [ItemAttributeRelationshipInline, ItemImagesInline]
    prepopulated_fields = {"slug": ("title", )}
    actions = [change_status]

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(ItemAdmin, self).get_queryset(request)

        return qs\
            .select_related('item_class', 'creator')\
            .prefetch_related('item_attr', 'item_attr__attribute_values', 'recommend_item')


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('title', 'on_item', 'enable')
    prepopulated_fields = {"slug": ("title", )}
    actions = [change_status]


class AttributeValueAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}


class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}
    list_display = ('title', 'parent', 'slug', 'sort', 'enable')
    actions = [change_status]

admin.site.register(Item, ItemAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(ItemClass)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeValue, AttributeValueAdmin)
