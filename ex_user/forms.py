__author__ = 'igor'
from ex_user.models import ExUser
from django import forms
from django.contrib.auth.models import User
from django.forms import HiddenInput


class ExUserForm(forms.ModelForm):
    user = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = ExUser
        fields = ['img', 'user']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']