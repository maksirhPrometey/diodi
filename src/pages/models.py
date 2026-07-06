from django.core.exceptions import ValidationError
from django.db import models

from src.core.models import OrderedModel, SEOMixin, SingletonModel


class HomePage(SingletonModel, SEOMixin):
    hero_title = models.CharField('Заголовок hero', max_length=255)
    intro_text = models.TextField('Вступний текст')
    benefits_title = models.CharField('Заголовок блоку переваг', max_length=255, blank=True)
    benefits_lead = models.TextField('Текст блоку переваг', blank=True)
    why_us_title = models.CharField('Заголовок «Чому ми»', max_length=200, blank=True)
    why_us_text = models.TextField('Текст «Чому ми»', blank=True)
    implant_cta_text = models.CharField('CTA імплантології', max_length=255, blank=True)
    implant_description = models.TextField('Опис імплантології', blank=True)
    implant_image = models.ImageField('Зображення імплант-блоку', upload_to='home/', blank=True)

    class Meta:
        verbose_name = 'Головна сторінка'
        verbose_name_plural = 'Головна сторінка'

    def __str__(self):
        return 'Головна'


class HomeGalleryImage(OrderedModel):
    home_page = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='Головна',
    )
    image = models.ImageField('Зображення', upload_to='home/gallery/')
    alt_text = models.CharField('Alt-текст', max_length=200, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Фото головної'
        verbose_name_plural = 'Фото головної'
        indexes = [models.Index(fields=['home_page', 'sort_order'])]

    def __str__(self):
        return self.alt_text or f'Фото #{self.pk}'


class AboutPage(SingletonModel, SEOMixin):
    title = models.CharField('Заголовок', max_length=200)
    body = models.TextField('Текст')
    image = models.ImageField('Зображення', upload_to='about/', blank=True)

    class Meta:
        verbose_name = 'Сторінка «Про нас»'
        verbose_name_plural = 'Сторінка «Про нас»'

    def __str__(self):
        return self.title


class LaboratoryPage(SingletonModel, SEOMixin):
    title = models.CharField('Заголовок', max_length=200)
    body = models.TextField('Текст')
    hero_image = models.ImageField('Hero-зображення', upload_to='laboratory/', blank=True)

    class Meta:
        verbose_name = 'Сторінка «Лабораторія»'
        verbose_name_plural = 'Сторінка «Лабораторія»'

    def __str__(self):
        return self.title


class ContactsPage(SingletonModel, SEOMixin):
    title = models.CharField('Заголовок', max_length=200)
    intro_text = models.TextField('Вступний текст', blank=True)
    use_site_settings = models.BooleanField(
        'Контакти з налаштувань сайту',
        default=True,
        help_text='Телефони, email і карта беруться з «Налаштування сайту».',
    )

    class Meta:
        verbose_name = 'Сторінка «Контакти»'
        verbose_name_plural = 'Сторінка «Контакти»'

    def __str__(self):
        return self.title


class ServicesIndexPage(SingletonModel, SEOMixin):
    title = models.CharField('Заголовок', max_length=200)
    intro_text = models.TextField('Вступний текст', blank=True)

    class Meta:
        verbose_name = 'Сторінка «Послуги»'
        verbose_name_plural = 'Сторінка «Послуги»'

    def __str__(self):
        return self.title


class Service(SEOMixin, OrderedModel):
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Батьківська послуга',
    )
    title = models.CharField('Назва', max_length=200)
    slug = models.SlugField('Slug', max_length=100, unique=True)
    short_description = models.CharField('Короткий опис', max_length=300, blank=True)
    body = models.TextField('Повний текст', blank=True)
    image = models.ImageField('Зображення', upload_to='services/', blank=True)
    is_featured = models.BooleanField(
        'У footer',
        default=False,
        help_text='Оберіть до 4 послуг для блоку «Послуги» у footer.',
    )
    legacy_path = models.CharField('Legacy URL', max_length=255, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'
        indexes = [
            models.Index(fields=['parent', 'sort_order']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        if self.parent:
            return f'{self.parent.title} → {self.title}'
        return self.title

    def clean(self):
        super().clean()
        if self.parent and self.parent.parent_id:
            raise ValidationError({'parent': 'Максимум 2 рівні вкладеності (категорія → підпослуга).'})
        if self.parent_id and self.pk and self.parent_id == self.pk:
            raise ValidationError({'parent': 'Послуга не може бути батьком сама собі.'})


class TeamRole(models.TextChoices):
    DIRECTOR = 'director', 'Директор'
    CHIEF_DOCTOR = 'chief_doctor', 'Головний лікар'
    DOCTOR = 'doctor', 'Лікар-стоматолог'
    DENTAL_TECHNICIAN = 'dental_technician', 'Зубний технік'
    ADMINISTRATOR = 'administrator', 'Адміністратор'
    NURSE = 'nurse', 'Середній медичний персонал'


class TeamMember(SEOMixin, OrderedModel):
    full_name = models.CharField('Повне імʼя', max_length=200)
    short_name = models.CharField('Коротке імʼя', max_length=50, blank=True)
    slug = models.SlugField('Slug', max_length=100, unique=True)
    role = models.CharField('Роль', max_length=30, choices=TeamRole.choices)
    role_title = models.CharField('Посада (UI)', max_length=200, blank=True)
    is_doctor = models.BooleanField(
        'Лікар',
        default=False,
        help_text='Показувати блок «Записатись до лікаря» на сторінці профілю.',
    )
    bio = models.TextField('Біографія', blank=True)
    photo = models.ImageField('Фото', upload_to='team/', blank=True)
    legacy_path = models.CharField('Legacy URL', max_length=255, blank=True)
    services = models.ManyToManyField(
        Service,
        blank=True,
        related_name='team_members',
        verbose_name='Послуги',
    )

    class Meta(OrderedModel.Meta):
        verbose_name = 'Член команди'
        verbose_name_plural = 'Команда'
        indexes = [
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return self.full_name


class Gallery(SEOMixin):
    title = models.CharField('Назва', max_length=200)
    slug = models.SlugField('Slug', max_length=50, unique=True)
    description = models.TextField('Опис', blank=True)

    class Meta:
        verbose_name = 'Фотогалерея'
        verbose_name_plural = 'Фотогалереї'

    def __str__(self):
        return self.title


class GalleryImage(OrderedModel):
    gallery = models.ForeignKey(
        Gallery,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Галерея',
    )
    image = models.ImageField('Зображення', upload_to='gallery/')
    alt_text = models.CharField('Alt-текст', max_length=200, blank=True)
    caption = models.CharField('Підпис', max_length=255, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Фото галереї'
        verbose_name_plural = 'Фото галереї'
        indexes = [models.Index(fields=['gallery', 'sort_order'])]

    def __str__(self):
        return self.caption or self.alt_text or f'Фото #{self.pk}'


class PriceList(SingletonModel):
    title = models.CharField('Заголовок', max_length=200)
    currency_label = models.CharField('Валюта', max_length=20, default='грн.')
    approval_note = models.CharField('Примітка про затвердження', max_length=255, blank=True)
    is_published = models.BooleanField('Опубліковано', default=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        verbose_name = 'Прейскурант'
        verbose_name_plural = 'Прейскурант'

    def __str__(self):
        return self.title


class PriceCategory(OrderedModel):
    price_list = models.ForeignKey(
        PriceList,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Прейскурант',
    )
    title = models.CharField('Категорія', max_length=200)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Категорія цін'
        verbose_name_plural = 'Категорії цін'

    def __str__(self):
        return self.title


class PriceItem(OrderedModel):
    class PriceType(models.TextChoices):
        EXACT = 'exact', 'Точна ціна'
        FROM = 'from', 'Від'
        RANGE = 'range', 'Діапазон'

    category = models.ForeignKey(
        PriceCategory,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Категорія',
    )
    name = models.CharField('Назва послуги', max_length=255)
    price_type = models.CharField('Тип ціни', max_length=10, choices=PriceType.choices, default=PriceType.EXACT)
    price = models.DecimalField('Ціна', max_digits=10, decimal_places=2, null=True, blank=True)
    price_max = models.DecimalField('Ціна (макс.)', max_digits=10, decimal_places=2, null=True, blank=True)
    note = models.CharField('Примітка', max_length=100, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Позиція прейскуранту'
        verbose_name_plural = 'Позиції прейскуранту'
        indexes = [models.Index(fields=['category', 'sort_order'])]

    def __str__(self):
        return self.name


class Review(models.Model):
    class Source(models.TextChoices):
        MANUAL = 'manual', 'Вручну'
        IMPORTED = 'imported', 'Імпорт'

    author_name = models.CharField('Автор', max_length=100)
    text = models.TextField('Текст відгуку')
    rating = models.PositiveSmallIntegerField('Оцінка (1–5)', null=True, blank=True)
    source = models.CharField('Джерело', max_length=20, choices=Source.choices, default=Source.MANUAL)
    is_published = models.BooleanField('Опубліковано', default=False)
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['is_published', '-created_at'])]

    def __str__(self):
        return self.author_name


class ContactSubmission(models.Model):
    FORM_CALLBACK = 'callback'
    FORM_EMAIL = 'email'
    FORM_CHOICES = [
        (FORM_CALLBACK, 'Замовити дзвінок'),
        (FORM_EMAIL, 'Написати нам'),
    ]

    form_type = models.CharField('Тип форми', max_length=20, choices=FORM_CHOICES, default=FORM_CALLBACK)
    name = models.CharField('Імʼя', max_length=100)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)
    message = models.TextField('Повідомлення')
    ip_address = models.GenericIPAddressField('IP-адреса', null=True, blank=True)
    is_processed = models.BooleanField('Оброблено', default=False)
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка з форми'
        verbose_name_plural = 'Заявки з форм'
        indexes = [models.Index(fields=['is_processed', '-created_at'])]

    def __str__(self):
        return f'{self.name} ({self.get_form_type_display()})'


class LegacyRedirect(models.Model):
    old_path = models.CharField('Старий шлях', max_length=255, unique=True)
    new_path = models.CharField('Новий шлях', max_length=255)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = 'Legacy redirect'
        verbose_name_plural = 'Legacy redirects'
        ordering = ['old_path']

    def __str__(self):
        return f'{self.old_path} → {self.new_path}'
