from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', views.DetailGroupView.as_view(), name='detail_group'),
    url(r'^(?P<group>[-\w]+)/(?P<slug>[-\w]+)/$', views.DetailItemView.as_view(), name='detail_item'),
]