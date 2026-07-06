"""Django sitemap-класи для sitemap.xml (seo_skill)."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from src.pages.models import Service, TeamMember


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return ['home', 'about', 'team', 'gallery', 'services', 'lab', 'prices', 'reviews', 'contacts']

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_published=True)

    def location(self, obj):
        return reverse('service_detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class TeamMemberSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.4

    def items(self):
        return TeamMember.objects.filter(is_published=True)

    def location(self, obj):
        return reverse('team_member', args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at
