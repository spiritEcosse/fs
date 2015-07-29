__author__ = 'igor'
from ex_user.models import ExUser
from django import forms
from django.contrib.auth.models import User
from djangular.styling.bootstrap3.forms import Bootstrap3Form
from djangular.forms import NgFormValidationMixin, NgModelForm
from django.utils.translation import ugettext_lazy as _


class UserMeta(type(NgModelForm), type(Bootstrap3Form)):
    pass


class ExUserForm(NgModelForm, NgFormValidationMixin, Bootstrap3Form):
    __metaclass__ = UserMeta
    form_name = 'ex_user_form'
    scope_prefix = 'ex_user_model'

    class Meta:
        model = ExUser
        fields = ['img']


class UserForm(NgModelForm, NgFormValidationMixin, Bootstrap3Form):
    __metaclass__ = UserMeta
    form_name = 'user_form'
    scope_prefix = 'user_model'

    def __init__(self, **kwargs):
        super(UserForm, self).__init__(**kwargs)
        self.fields['password'].help_text = ''

        for name, type_field in self.fields.items():
            for error, message in type_field.get_potential_errors():
                if message.capitalize() and not self.fields[name].help_text:
                    self.fields[name].help_text += message.capitalize()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
