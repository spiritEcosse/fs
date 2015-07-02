__author__ = 'igor'

from django.conf.urls import include, url
from ex_user.views import Account
from django.contrib.auth import views as auth_views
from fs.core.ex_view import ExView


urlpatterns = [
    url(r'^$', Account.profile, name='profile'),
]