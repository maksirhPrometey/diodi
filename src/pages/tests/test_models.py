"""Тести моделей: singleton-поведінка, валідація дерева послуг, legacy redirect."""

import pytest
from django.core.exceptions import ValidationError

from src.core.models import SiteSettings
from src.pages.cms import parse_about_sections, format_price, services_home_intro
from src.pages.legacy_import import pick_laboratory_hero_image
from src.pages.models import LegacyRedirect, PriceItem, Service


def test_services_home_intro_ends_with_zub():
    intro = (
        'Клініка «ДіОДі» в Івано-Франківську турбується про кожного з пацієнтів. '
        'Наші лікарі використовують лише сучасні та ефективні методи лікування. '
        'Ми беремо на себе відповідальність за кожну зроблену роботу, за кожен ваш зуб. '
        'Тому в нашій клініці ви зможете отримати всі види послуг.'
    )
    assert services_home_intro(intro).endswith('за кожен ваш зуб!')


def test_format_price_appends_grn():
    item = PriceItem(name='Консультація', price_type=PriceItem.PriceType.EXACT, price=450)
    assert format_price(item) == '450 грн.'


def test_format_price_from_range_with_grn():
    item = PriceItem(
        name='Видалення',
        price_type=PriceItem.PriceType.RANGE,
        price=1000,
        price_max=3500,
    )
    assert format_price(item) == '1 000 – 3 500 грн.'


def test_format_price_implant_uses_uo():
    item = PriceItem(
        name='Постановка одного імпланту',
        price_type=PriceItem.PriceType.FROM,
        price=400,
        note='у.о',
    )
    assert format_price(item) == 'від 400 у.о.'


def test_parse_about_sections_plain_paragraphs_have_no_title():
    body = 'Перший абзац.\n\nДругий абзац.'
    sections = parse_about_sections(body)
    assert len(sections) == 2
    assert sections[0]['title'] == ''
    assert sections[1]['title'] == ''


def test_parse_about_sections_explicit_title():
    body = 'Наш підхід\nТекст під заголовком.'
    sections = parse_about_sections(body)
    assert sections[0]['title'] == 'Наш підхід'
    assert sections[0]['text'] == 'Текст під заголовком.'


def test_pick_laboratory_hero_image_prefers_logo():
    images = [
        '../images/laboratoriya/LOGO-DIOLAB-600.jpg',
        '../images/laboratoriya/lab-01.jpg',
        '../images/laboratoriya/lab-02.jpg',
    ]
    assert pick_laboratory_hero_image(images).endswith('LOGO-DIOLAB-600.jpg')


def test_pick_laboratory_hero_image_fallback_first():
    images = [
        '../images/laboratoriya/lab-01.jpg',
        '../images/laboratoriya/lab-02.jpg',
    ]
    assert pick_laboratory_hero_image(images).endswith('lab-01.jpg')


@pytest.mark.django_db
def test_singleton_load_creates_pk_one():
    settings_obj = SiteSettings.load()
    assert settings_obj.pk == 1


@pytest.mark.django_db
def test_years_of_experience_label_from_founded_year():
    settings_obj = SiteSettings.load()
    settings_obj.founded_year = 2001
    settings_obj.save()
    assert settings_obj.years_of_experience_label.endswith('+')
    assert settings_obj.years_of_experience >= 24
    assert settings_obj.lab_brand_name == 'Dio-Lab'


@pytest.mark.django_db
def test_singleton_load_is_idempotent():
    first = SiteSettings.load()
    second = SiteSettings.load()
    assert first.pk == second.pk == 1
    assert SiteSettings.objects.count() == 1


@pytest.mark.django_db
def test_singleton_save_always_forces_pk_one():
    settings_obj = SiteSettings.load()
    settings_obj.pk = 999
    settings_obj.save()
    assert settings_obj.pk == 1
    assert SiteSettings.objects.count() == 1


@pytest.mark.django_db
def test_service_rejects_three_level_nesting():
    root = Service.objects.create(title='Терапія', slug='terapiya')
    child = Service.objects.create(title='Пломбування', slug='plombuvannya', parent=root)
    grandchild = Service(title='Підпункт', slug='pidpunkt', parent=child)
    with pytest.raises(ValidationError):
        grandchild.clean()


@pytest.mark.django_db
def test_service_rejects_self_parent():
    service = Service.objects.create(title='Ортопедія', slug='ortopediya')
    service.parent_id = service.pk
    with pytest.raises(ValidationError):
        service.clean()


@pytest.mark.django_db
def test_legacy_redirect_str():
    redirect = LegacyRedirect.objects.create(old_path='/old/', new_path='/new/')
    assert str(redirect) == '/old/ → /new/'
