from django.conf.urls import include, url
from django.contrib import admin
from fs import settings
from django.conf.urls.static import static
from fs.views import IndexView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # url(r'^search/', include('haystack.urls')),
    url(r'^search/',
        include('search.urls', app_name='search', namespace='search')),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^profile/',
        include('ex_user.urls', app_name='ex_user', namespace='ex_user')),
    url('^', include('django.contrib.auth.urls')),
    url(r'^materials/',
        include('materials.urls', app_name='materials',
                namespace='materials')),
    url(r'^comments/',
        include('comments.urls', app_name='comments', namespace='comments')),
    url(r'^admin/', include(admin.site.urls)),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
