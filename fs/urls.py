from django.conf.urls import include, url
from django.contrib import admin
from fs import settings
from django.conf.urls.static import static
from fs.views import IndexView
from django.contrib.auth import views as auth_views
from fs.core.ex_view import ExView
from ex_user.views import Account

urlpatterns = [
    url(r'^$', IndexView.as_view(), ExView.extra_context_data(), name='home'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^profile/$', Account.profile, {'extra_context': ExView.extra_context_data()}, name='profile'),
    url(r'^password_change/$', auth_views.password_change,
        {'extra_context': ExView.extra_context_data()}),
    url('^', include('django.contrib.auth.urls'), {'extra_context': ExView.extra_context_data()}),
    url(r'^materials/', include('materials.urls', app_name='materials', namespace='materials'),
        {'extra_context': ExView.extra_context_data()}),
    url(r'^comments/', include('comments.urls', app_name='comments', namespace='comments')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)