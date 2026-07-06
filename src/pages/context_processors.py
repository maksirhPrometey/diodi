from django.conf import settings as django_settings

from src.core.models import SiteSettings, SocialLink
from src.pages.cms import build_ld_json, dentist_schema, published_services_qs, service_to_card, service_to_mega
from src.pages.models import HomePage


def site_settings(request):
    settings_obj = SiteSettings.load()
    social_links = list(
        SocialLink.objects.filter(site_settings=settings_obj).order_by('sort_order', 'pk')
    )
    home_page = HomePage.objects.filter(is_published=True).first()
    root_services = list(published_services_qs())
    footer_services = root_services[:4]
    footer_text = ''
    if home_page and home_page.intro_text:
        footer_text = home_page.intro_text
        if len(footer_text) > 180:
            footer_text = f'{footer_text[:177].rstrip()}…'
    external_links = [link for link in social_links if link.platform == SocialLink.Platform.EXTERNAL]
    social_only = [link for link in social_links if link.platform != SocialLink.Platform.EXTERNAL]
    return {
        'site_settings': settings_obj,
        'featured_services': [service_to_card(s, i) for i, s in enumerate(footer_services)],
        'footer_services': [{'slug': s.slug, 'title': s.title} for s in footer_services],
        'footer_text': footer_text,
        'social_links': social_only,
        'external_links': external_links,
        'mega_services': [service_to_mega(s) for s in root_services],
        'recaptcha_site_key': django_settings.RECAPTCHA_SITE_KEY,
        'dentist_schema_json': build_ld_json(dentist_schema(request, settings_obj)),
    }
