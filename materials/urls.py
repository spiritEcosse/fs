from django.conf.urls import include, url
from . import views
from urlbreadcrumbs import url as burl

urlpatterns = [
    url(r'^(?P<group_slug>[-\w]+(/[\w-]+)*)/item/(?P<slug>[-\w]+)/$',
        views.DetailItemView.as_view(), name='detail_item'),
    url(r'^(?P<slug>[\w-]+(/[\w-]+)*)/$',
        views.DetailGroupView.as_view(), name='detail_group'),
]