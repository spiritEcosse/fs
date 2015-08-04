from django.conf.urls import include, url
from materials import views

urlpatterns = [
    url(r'^attribute/(?P<group_slug>[-\w]+)/(?P<slug>[\w-]+)/$', views.AttributeDetailView.as_view(), name='attribute'),
    url(r'^item/(?P<group_slug>[-\w]+(/[\w-]+)*)/(?P<slug>[-\w]+)/$',
        views.DetailItemView.as_view(), name='detail_item'),
    url(r'^group/(?P<slug>[\w-]+(/[\w-]+)*)/$',
        views.DetailGroupView.as_view(), name='detail_group'),
    url(r'^favorite_item/(?P<pk>[\d]+)/$', views.FavoriteItem.as_view(), name='favorite_item'),
    url(r'^future_item/(?P<pk>[\d]+)/$', views.FutureItem.as_view(), name='future_item'),
    url(r'^add_content_type/$', views.AddContentType.as_view(), name='add_content_type'),
    url(r'^play_video/(?P<group_slug>[-\w]+(/[\w-]+)*)/(?P<slug>[-\w]+)/$',
        views.PlayVideo.as_view(), name='play_video'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^cancel_vote/', views.cancel_vote, name='cancel_vote'),
    url(r'^edit/(?P<slug>[-\w]+)/$', views.EditItemView.as_view(), name='item_edit')
]