from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'microstructure.views.home', name='home'),
    url(r'^programs(?:.html)?$', 'microstructure.views.programs', name='programs'),
    url(r'^program/([0-9]{1,4})(?:.html)?$', 'microstructure.views.program', name='program'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
