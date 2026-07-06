"""Smoke-тести: усі публічні сторінки повертають 200, legacy redirect працює."""

import pytest

from src.pages.models import LegacyRedirect

PUBLIC_URLS = [
    '/',
    '/pro-nas/',
    '/pro-nas/nasha-komanda/',
    '/pro-nas/fotohalereia/',
    '/posluhy/',
    '/labaratoriia/',
    '/tsiny/',
    '/vidhuky/',
    '/kontakty/',
]


@pytest.mark.django_db
@pytest.mark.parametrize('url', PUBLIC_URLS)
def test_public_page_returns_200(client, seed_content, url):
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_service_detail_returns_200(client, seed_content):
    service = seed_content['service']
    response = client.get(f'/posluhy/{service.slug}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_team_member_detail_returns_200(client, seed_content):
    member = seed_content['member']
    response = client.get(f'/pro-nas/nasha-komanda/{member.slug}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_unknown_service_slug_redirects_to_services(client, seed_content):
    response = client.get('/posluhy/nemaie-takoi-poslugy/')
    assert response.status_code == 302
    assert response.url == '/posluhy/'


@pytest.mark.django_db
def test_legacy_redirect_middleware(client):
    LegacyRedirect.objects.create(old_path='/stara-storinka/', new_path='/posluhy/')
    response = client.get('/stara-storinka/')
    assert response.status_code == 301
    assert response.url == '/posluhy/'


@pytest.mark.django_db
def test_sitemap_xml_returns_200(client, seed_content):
    response = client.get('/sitemap.xml')
    assert response.status_code == 200
    assert response['Content-Type'].startswith('application/xml')


@pytest.mark.django_db
def test_robots_txt_returns_200(client):
    response = client.get('/robots.txt')
    assert response.status_code == 200
    assert b'Sitemap:' in response.content
