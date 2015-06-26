from django.conf.urls import include, url
from materials import views

urlpatterns = [
    url(r'^attribute/(?P<group_slug>[-\w]+)/(?P<slug>[\w-]+)/$', views.AttributeDetailView.as_view(), name='attribute'),
    url(r'^item/(?P<group_slug>[-\w]+(/[\w-]+)*)/(?P<slug>[-\w]+)/$',
        views.ItemDetail.as_view(), name='detail_item'),
    url(r'^group/(?P<slug>[\w-]+(/[\w-]+)*)/$',
        views.DetailGroupView.as_view(), name='detail_group'),
]