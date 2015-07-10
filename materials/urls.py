from django.conf.urls import include, url
from materials import views

urlpatterns = [
    url(r'^attribute/(?P<group_slug>[-\w]+)/(?P<slug>[\w-]+)/$', views.AttributeDetailView.as_view(), name='attribute'),
    url(r'^item/(?P<group_slug>[-\w]+(/[\w-]+)*)/(?P<slug>[-\w]+)/$',
        views.ItemDetail.as_view(), name='detail_item'),
    url(r'^group/(?P<slug>[\w-]+(/[\w-]+)*)/$',
        views.DetailGroupView.as_view(), name='detail_group'),
    url(r'^put_item/$', views.put_item, name='put_item'),
    url(r'^play_video/(?P<group_slug>[-\w]+(/[\w-]+)*)/(?P<slug>[-\w]+)/$',
        views.PlayVideo.as_view(), name='play_video'),
    url(r'^del_item/$', views.del_item, name='del_item'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^cancel_vote/', views.cancel_vote, name='cancel_vote')
]