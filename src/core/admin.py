from django.contrib import admin
from unfold.admin import TabularInline

from src.core.admin_mixins import SEO_FIELDSET, SEO_READONLY, SingletonModelAdmin, admin_image_preview
from src.core.models import SiteSettings, SocialLink


class SocialLinkInline(TabularInline):
    model = SocialLink
    extra = 0
    ordering = ('sort_order',)
    fields = ('platform', 'label', 'url', 'sort_order')


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    inlines = [SocialLinkInline]
    readonly_fields = ('logo_preview', 'default_og_preview', *SEO_READONLY)

    fieldsets = (
        ('Бренд', {
            'fields': ('site_name', 'logo', 'logo_preview', 'copyright_text', 'default_og_image', 'default_og_preview'),
        }),
        ('Контакти', {
            'fields': ('phone_primary', 'phone_secondary', 'email', 'address'),
        }),
        ('Графік роботи', {
            'fields': ('schedule_weekdays', 'schedule_saturday', 'schedule_sunday'),
        }),
        ('Карта', {
            'fields': ('latitude', 'longitude', 'map_embed_url'),
        }),
        SEO_FIELDSET,
        ('Системне', {
            'classes': ('collapse',),
            'fields': SEO_READONLY,
        }),
    )

    logo_preview = admin_image_preview('logo')
    default_og_preview = admin_image_preview('default_og_image')
