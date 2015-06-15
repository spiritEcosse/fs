from django.conf.urls import include, url
from django.contrib import admin
from fs import settings
from django.conf.urls.static import static
from fs.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^materials/', include('materials.urls', app_name='materials', namespace='materials')),
    url(r'^comments/', include('comments.urls', app_name='comments', namespace='comments')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)