"""Спільні фікстури для smoke-тестів src/pages."""

import pytest

from src.core.models import SiteSettings
from src.pages.models import (
    AboutPage,
    ContactsPage,
    HomePage,
    LaboratoryPage,
    PriceCategory,
    PriceItem,
    PriceList,
    Service,
    ServicesIndexPage,
    TeamMember,
    TeamRole,
)


@pytest.fixture
def site_settings(db):
    return SiteSettings.load()


@pytest.fixture
def seed_content(db, site_settings):
    """Мінімальний набір опублікованих сторінок і сутностей для view-тестів."""
    HomePage.objects.create(
        pk=1,
        hero_title='Вас вітає клініка «ДіОДі»',
        intro_text='Повний спектр стоматологічних послуг в Івано-Франківську.',
    )
    AboutPage.objects.create(pk=1, title='Про клініку', body='Клініка «ДіОДі» з 2001 року.')
    LaboratoryPage.objects.create(pk=1, title='Лабораторія Dio-Lab', body='Власна лабораторія CAD/CAM.')
    ContactsPage.objects.create(pk=1, title='Контакти', intro_text='Звʼяжіться з нами.')
    ServicesIndexPage.objects.create(pk=1, title='Послуги', intro_text='Наші послуги.')

    price_list = PriceList.objects.create(pk=1, title='Прейскурант')
    category = PriceCategory.objects.create(price_list=price_list, title='Терапія')
    PriceItem.objects.create(category=category, name='Пломба', price=500)

    service = Service.objects.create(title='Імплантологія', slug='implantologiya', short_description='Опис')
    member = TeamMember.objects.create(
        full_name='Тестовий Лікар',
        slug='testovyi-likar',
        role=TeamRole.DOCTOR,
        is_doctor=True,
    )
    return {'service': service, 'member': member}
