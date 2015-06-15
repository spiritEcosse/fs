from django.conf.urls import include, url
from materials import views

urlpatterns = [
    # url(r'^(?)$'),
    url(r'^(?P<group_slug>[-\w]+(/[\w-]+)*)/item/(?P<slug>[-\w]+)/$',
        views.ItemDetail.as_view(), name='detail_item'),
    url(r'^(?P<slug>[\w-]+(/[\w-]+)*)/$',
        views.DetailGroupView.as_view(), name='detail_group'),
]