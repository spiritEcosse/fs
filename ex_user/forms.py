__author__ = 'igor'
from ex_user.models import ExUser
from django import forms
from django.contrib.auth.models import User
from djangular.styling.bootstrap3.forms import Bootstrap3Form
from djangular.forms import NgFormValidationMixin, NgModelForm


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

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']