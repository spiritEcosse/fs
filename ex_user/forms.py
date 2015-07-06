__author__ = 'igor'
from ex_user.models import ExUser
from django import forms
from django.contrib.auth.models import User


class ExUserForm(forms.ModelForm):
    class Meta:
        model = ExUser
        fields = ['img']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']