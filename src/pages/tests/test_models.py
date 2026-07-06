"""Тести моделей: singleton-поведінка, валідація дерева послуг, legacy redirect."""

import pytest
from django.core.exceptions import ValidationError

from src.core.models import SiteSettings
from src.pages.legacy_import import pick_laboratory_hero_image
from src.pages.models import LegacyRedirect, Service


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
