from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path
from django.views.generic import TemplateView

from src.pages.sitemaps import ServiceSitemap, StaticViewSitemap, TeamMemberSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'team': TeamMemberSitemap,
}

urlpatterns = [
    path('healthz/', lambda request: HttpResponse('ok')),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path(
        'robots.txt',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
        name='robots_txt',
    ),
    path('', include('src.pages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
