from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.template import defaultfilters


class ImageWidget(forms.FileInput):
    """
    A ImageField Widget that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a class="thumbnail" href="%s">'
                           '<img src="%s" style="max-width:%s; max-height:%s;" /></a>'
                           % (value.url, value.url, self.attrs['max_width'], self.attrs['max_height'])))
        output.append(super(ImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class MultipleChoiceWidget(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        self.choices.queryset = self.choices.queryset.filter(pk__in=value)
        output = ''

        for obj in self.choices.queryset:
            output += ('<button class="btn btn-primary btn-xs block" onclick="$(this).remove()" >'
                       '<input name="%s" type="hidden" value="%d" >%s '
                       '<span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button>') \
                      % (name, obj.pk, obj.get_name())
        output += ('<button class="add_content" class="btn bnt-default btn-sm" id="add_content_type" '
                   'data-name-field="%s" data-model="%s">'
                   '<span class="glyphicon glyphicon-plus"></span>'
                   + unicode(_('Add')) + ' %s</button>') % (name, self.choices.queryset.model._meta.model_name, name, )
        return mark_safe(output)


class DateWidget(forms.DateInput):
    def render(self, name, value, attrs=None):
        output = ('<div class="form-group">'
                  ' <div class="input-group date" id="datetimepicker">'
                  '     <input type="text" name="%s" class="form-control" value="%s"/>'
                  '     <span class="input-group-addon">'
                  '         <span class="glyphicon glyphicon-calendar"></span>'
                  '     </span>'
                  ' </div>'
                  '</div>' % (name, value))
        return mark_safe(output)