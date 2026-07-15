from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
import re


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj


class SEOMixin(models.Model):
    meta_title = models.CharField('Meta title', max_length=70, blank=True)
    meta_description = models.CharField('Meta description', max_length=160, blank=True)
    og_title = models.CharField('OG title', max_length=70, blank=True)
    og_description = models.CharField('OG description', max_length=200, blank=True)
    og_image = models.ImageField('OG image', upload_to='seo/', blank=True)
    canonical_url = models.URLField('Canonical URL', blank=True)
    is_published = models.BooleanField('Опубліковано', default=True)
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        abstract = True
        ordering = ['sort_order', 'pk']
        indexes = [models.Index(fields=['sort_order'])]


class SiteSettings(SingletonModel, SEOMixin):
    site_name = models.CharField('Назва сайту', max_length=100, default='Стоматологія «ДіОДі»')
    phone_primary = models.CharField('Телефон (основний)', max_length=20, default='(050) 537-76-57')
    phone_secondary = models.CharField('Телефон (додатковий)', max_length=20, blank=True, default='(067) 343-60-10')
    email = models.EmailField('Email', default='diodi2001@gmail.com')
    logo = models.ImageField('Логотип', upload_to='site/', blank=True)
    address = models.CharField('Адреса', max_length=255, blank=True)
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('Довгота', max_digits=9, decimal_places=6, null=True, blank=True)
    map_embed_url = models.URLField(
        'URL карти (iframe)',
        blank=True,
        default=(
            'https://www.openstreetmap.org/export/embed.html?'
            'bbox=24.665%2C48.898%2C24.697%2C48.912&layer=mapnik&marker=48.905185%2C24.680990'
        ),
    )
    schedule_weekdays = models.CharField('Графік (Пн–Пт)', max_length=100, blank=True, default='9:30 – 21:00')
    schedule_saturday = models.CharField('Графік (Сб)', max_length=100, blank=True, default='за записом')
    schedule_sunday = models.CharField('Графік (Нд)', max_length=100, blank=True, default='вихідний')
    copyright_text = models.CharField(
        'Copyright',
        max_length=255,
        blank=True,
        default='© Стоматологія «ДіОДі», Івано-Франківськ',
    )
    founded_year = models.PositiveSmallIntegerField(
        'Рік заснування',
        default=2001,
        help_text='Для статистики «років досвіду» на головній і в «Про клініку».',
    )
    lab_brand_name = models.CharField(
        'Назва лабораторії',
        max_length=50,
        default='Dio-Lab',
        help_text='Бренд власної зуботехнічної лабораторії (hero / about).',
    )
    default_og_image = models.ImageField('OG image за замовчуванням', upload_to='seo/', blank=True)

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self):
        return self.site_name

    @property
    def years_of_experience(self) -> int:
        current_year = timezone.now().year
        return max(current_year - int(self.founded_year or 2001), 0)

    @property
    def years_of_experience_label(self) -> str:
        return f'{self.years_of_experience}+'

    @property
    def phone_primary_href(self):
        return self._tel_href(self.phone_primary)

    @property
    def phone_secondary_href(self):
        return self._tel_href(self.phone_secondary)

    @property
    def phone_primary_display(self):
        return self._phone_display(self.phone_primary)

    @property
    def phone_secondary_display(self):
        return self._phone_display(self.phone_secondary)

    @staticmethod
    def normalize_phone(value: str) -> str:
        cleaned = re.sub(r'^\+?38\s*', '', (value or '').strip())
        return cleaned.strip()

    @staticmethod
    def _phone_display(value: str) -> str:
        local = SiteSettings.normalize_phone(value)
        if not local:
            return ''
        return f'+38 {local}'

    @staticmethod
    def _tel_href(value):
        digits = ''.join(ch for ch in value if ch.isdigit())
        if digits.startswith('380'):
            return f'tel:+{digits}'
        if digits.startswith('0'):
            return f'tel:+38{digits}'
        return f'tel:{value}'


class SocialLink(OrderedModel):
    class Platform(models.TextChoices):
        INSTAGRAM = 'instagram', 'Instagram'
        FACEBOOK = 'facebook', 'Facebook'
        EXTERNAL = 'external', 'Зовнішній ресурс'

    site_settings = models.ForeignKey(
        SiteSettings,
        on_delete=models.CASCADE,
        related_name='social_links',
        verbose_name='Налаштування сайту',
    )
    platform = models.CharField('Платформа', max_length=20, choices=Platform.choices)
    label = models.CharField('Підпис', max_length=50)
    url = models.URLField('Посилання')

    class Meta(OrderedModel.Meta):
        verbose_name = 'Соцмережа'
        verbose_name_plural = 'Соцмережі'
        constraints = [
            models.UniqueConstraint(
                fields=['site_settings', 'platform'],
                name='unique_social_platform_per_site',
            ),
        ]

    def __str__(self):
        return f'{self.label} ({self.get_platform_display()})'
