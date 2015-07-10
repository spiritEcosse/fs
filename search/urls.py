__author__ = 'igor'
from django.conf.urls import include, url
from search.views import MySearchView
from search import views

urlpatterns = [
    url(r'^$', MySearchView.as_view(), name='index'),
    url(r'^autocomplete/$', views.autocomplete, name='autocomplete'),
]