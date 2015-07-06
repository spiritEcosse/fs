__author__ = 'igor'
from comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django import forms


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'like_object']
        widgets = {
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

