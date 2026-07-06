"""Конфігурація django-unfold для ДіОДі CMS."""

from django.templatetags.static import static
from django.urls import reverse_lazy


def environment_callback(request):
    from django.conf import settings
    if settings.DEBUG:
        return ['Розробка', 'warning']
    return ['Production', 'success']


UNFOLD = {
    'SITE_TITLE': 'ДіОДі',
    'SITE_HEADER': 'ДіОДі CMS',
    'SITE_SUBHEADER': 'Керування контентом клініки',
    'SITE_URL': '/',
    'SITE_SYMBOL': 'dentistry',
    'SHOW_HISTORY': True,
    'SHOW_VIEW_ON_SITE': True,
    'ENVIRONMENT': 'config.unfold_settings.environment_callback',
    'LOGIN': {
        'redirect_after': lambda request: reverse_lazy('admin:index'),
    },
    'COLORS': {
        'primary': {
            '50': '240 249 255',
            '100': '224 242 254',
            '200': '186 230 253',
            '300': '87 181 200',
            '400': '0 136 204',
            '500': '0 120 210',
            '600': '0 110 199',
            '700': '3 89 162',
            '800': '0 62 113',
            '900': '0 40 71',
            '950': '0 25 45',
        },
    },
    'SIDEBAR': {
        'show_search': True,
        'command_search': True,
        'show_all_applications': False,
        'navigation': [
            {
                'title': 'Налаштування',
                'items': [
                    {
                        'title': 'Сайт і контакти',
                        'icon': 'settings',
                        'link': reverse_lazy('admin:core_sitesettings_changelist'),
                    },
                ],
            },
            {
                'title': 'Сторінки',
                'separator': True,
                'items': [
                    {
                        'title': 'Головна',
                        'icon': 'home',
                        'link': reverse_lazy('admin:pages_homepage_changelist'),
                    },
                    {
                        'title': 'Про нас',
                        'icon': 'info',
                        'link': reverse_lazy('admin:pages_aboutpage_changelist'),
                    },
                    {
                        'title': 'Послуги (індекс)',
                        'icon': 'medical_services',
                        'link': reverse_lazy('admin:pages_servicesindexpage_changelist'),
                    },
                    {
                        'title': 'Лабораторія',
                        'icon': 'science',
                        'link': reverse_lazy('admin:pages_laboratorypage_changelist'),
                    },
                    {
                        'title': 'Контакти',
                        'icon': 'call',
                        'link': reverse_lazy('admin:pages_contactspage_changelist'),
                    },
                    {
                        'title': 'Прейскурант',
                        'icon': 'payments',
                        'link': reverse_lazy('admin:pages_pricelist_changelist'),
                    },
                ],
            },
            {
                'title': 'Контент',
                'separator': True,
                'items': [
                    {
                        'title': 'Послуги',
                        'icon': 'healing',
                        'link': reverse_lazy('admin:pages_service_changelist'),
                    },
                    {
                        'title': 'Команда',
                        'icon': 'groups',
                        'link': reverse_lazy('admin:pages_teammember_changelist'),
                    },
                    {
                        'title': 'Фотогалерея',
                        'icon': 'photo_library',
                        'link': reverse_lazy('admin:pages_gallery_changelist'),
                    },
                    {
                        'title': 'Категорії цін',
                        'icon': 'sell',
                        'link': reverse_lazy('admin:pages_pricecategory_changelist'),
                    },
                    {
                        'title': 'Відгуки',
                        'icon': 'reviews',
                        'link': reverse_lazy('admin:pages_review_changelist'),
                    },
                ],
            },
            {
                'title': 'Заявки',
                'separator': True,
                'items': [
                    {
                        'title': 'Форми з сайту',
                        'icon': 'inbox',
                        'link': reverse_lazy('admin:pages_contactsubmission_changelist'),
                    },
                ],
            },
            {
                'title': 'SEO',
                'separator': True,
                'items': [
                    {
                        'title': 'Legacy redirects',
                        'icon': 'link',
                        'link': reverse_lazy('admin:pages_legacyredirect_changelist'),
                    },
                ],
            },
            {
                'title': 'Система',
                'separator': True,
                'collapsible': True,
                'items': [
                    {
                        'title': 'Користувачі',
                        'icon': 'person',
                        'link': reverse_lazy('admin:auth_user_changelist'),
                    },
                    {
                        'title': 'Групи',
                        'icon': 'group',
                        'link': reverse_lazy('admin:auth_group_changelist'),
                    },
                ],
            },
        ],
    },
    'STYLES': [
        lambda request: static('css/admin/diodi.css'),
    ],
}
