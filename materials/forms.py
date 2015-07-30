__author__ = 'igor'
from comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django import forms
from materials.models import Item
from django.contrib.admin import widgets
from materials.models import Genre
from materials.widgets import ImageWidget, MultipleChoiceWidget, DateWidget
from djangular.forms import NgFormValidationMixin, NgModelForm
from djangular.styling.bootstrap3.forms import Bootstrap3Form


class UserMeta(type(NgModelForm), type(Bootstrap3Form)):
    pass


class CommentForm(NgModelForm, NgFormValidationMixin, Bootstrap3Form):
    __metaclass__ = UserMeta

    class Meta:
        model = Comment
        fields = ['text', 'like_object']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': _('You comment')})
        }
        error_messages = {
            'text': {
                'require': _("This field required."),
                },
            }


class EditItemForm(NgModelForm, NgFormValidationMixin, Bootstrap3Form):
    __metaclass__ = UserMeta

    class Meta:
        model = Item
        fields = ['title', 'origin_title', 'genres', 'main_image', 'description',
                  'year_release', 'countries']
        labels = {
            'origin_title': _('Original name (do not fill in if the same as Russian):'),
        }
        widgets = {
            'main_image': ImageWidget(attrs={'max_width': 'auto', 'max_height': 'auto'}),
            'genres': MultipleChoiceWidget,
            'countries': MultipleChoiceWidget,
            'year_release': DateWidget,
            'description': forms.Textarea(attrs={'class': "form-control"}),
            'title': forms.TextInput(attrs={'size': 40, 'title': _('Title'), 'class': "form-control"}),
            'origin_title': forms.TextInput(attrs={'size': 40, 'title': _('Origin title'), 'class': "form-control"}),
        }