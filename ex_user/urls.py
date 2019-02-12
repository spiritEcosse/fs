__author__ = 'igor'

from django.conf.urls import include, url
from ex_user.views import ExUser, ExUserRegistrationFormView


urlpatterns = [
    url(r'^$', ExUser.as_view(), name='profile'),
    url(r'^registration/$', ExUserRegistrationFormView.as_view(), name='registration'),
]