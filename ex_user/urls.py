__author__ = 'igor'

from django.conf.urls import include, url
from ex_user.views import ExUser, ExUserRegistrationFormView
from django.contrib.auth import views as auth_views
from fs.core.ex_view import ExView


urlpatterns = [
    url(r'^$', ExUser.profile, name='profile'),
    url(r'^registration/$', ExUserRegistrationFormView.as_view(), name='registration'),
]