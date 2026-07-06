from django.contrib import admin, messages
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from src.core.admin_mixins import SEO_FIELDSET, SEO_READONLY, SingletonModelAdmin, admin_image_preview
from src.pages.models import (
    AboutPage,
    ContactSubmission,
    ContactsPage,
    Gallery,
    GalleryImage,
    HomeGalleryImage,
    HomePage,
    LaboratoryPage,
    LegacyRedirect,
    PriceCategory,
    PriceItem,
    PriceList,
    Review,
    Service,
    ServicesIndexPage,
    TeamMember,
)


class OrderedTabularInline(TabularInline):
    ordering = ('sort_order',)
    extra = 0


class HomeGalleryImageInline(OrderedTabularInline):
    model = HomeGalleryImage
    fields = ('image', 'alt_text', 'sort_order')


@admin.register(HomePage)
class HomePageAdmin(SingletonModelAdmin):
    inlines = [HomeGalleryImageInline]
    readonly_fields = ('implant_image_preview', *SEO_READONLY)

    fieldsets = (
        ('Hero', {
            'fields': ('hero_title', 'intro_text'),
        }),
        ('Блок переваг', {
            'fields': ('benefits_title', 'benefits_lead'),
        }),
        ('Блок «Чому ми»', {
            'fields': ('why_us_title', 'why_us_text'),
        }),
        ('Імплантологія', {
            'fields': ('implant_cta_text', 'implant_description', 'implant_image', 'implant_image_preview'),
        }),
        SEO_FIELDSET,
        ('Системне', {
            'classes': ('collapse',),
            'fields': SEO_READONLY,
        }),
    )

    implant_image_preview = admin_image_preview('implant_image', 'admin-preview admin-preview--lg')


@admin.register(AboutPage)
class AboutPageAdmin(SingletonModelAdmin):
    readonly_fields = ('image_preview', *SEO_READONLY)
    fieldsets = (
        (None, {'fields': ('title', 'body', 'image', 'image_preview')}),
        SEO_FIELDSET,
        ('Системне', {'classes': ('collapse',), 'fields': SEO_READONLY}),
    )

    image_preview = admin_image_preview('image', 'admin-preview admin-preview--lg')


@admin.register(LaboratoryPage)
class LaboratoryPageAdmin(SingletonModelAdmin):
    readonly_fields = ('hero_image_preview', *SEO_READONLY)
    fieldsets = (
        (None, {'fields': ('title', 'body', 'hero_image', 'hero_image_preview')}),
        SEO_FIELDSET,
        ('Системне', {'classes': ('collapse',), 'fields': SEO_READONLY}),
    )

    hero_image_preview = admin_image_preview('hero_image', 'admin-preview admin-preview--lg')


@admin.register(ContactsPage)
class ContactsPageAdmin(SingletonModelAdmin):
    readonly_fields = SEO_READONLY
    fieldsets = (
        (None, {'fields': ('title', 'intro_text', 'use_site_settings')}),
        SEO_FIELDSET,
        ('Системне', {'classes': ('collapse',), 'fields': SEO_READONLY}),
    )


@admin.register(ServicesIndexPage)
class ServicesIndexPageAdmin(SingletonModelAdmin):
    readonly_fields = SEO_READONLY
    fieldsets = (
        (None, {'fields': ('title', 'intro_text')}),
        SEO_FIELDSET,
        ('Системне', {'classes': ('collapse',), 'fields': SEO_READONLY}),
    )


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ('title_with_level', 'slug', 'is_featured', 'is_published', 'sort_order')
    list_filter = ('is_featured', 'is_published', 'parent')
    search_fields = ('title', 'slug', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('parent',)
    readonly_fields = ('image_preview', *SEO_READONLY)
    ordering = ('sort_order', 'title')
    list_filter_submit = True

    fieldsets = (
        (None, {
            'fields': (
                'parent', 'title', 'slug', 'short_description',
                'body', 'image', 'image_preview', 'is_featured', 'sort_order', 'legacy_path',
            ),
        }),
        SEO_FIELDSET,
        ('Системне', {'classes': ('collapse',), 'fields': SEO_READONLY}),
    )

    image_preview = admin_image_preview('image', 'admin-preview admin-preview--lg')

    @admin.display(description='Назва')
    def title_with_level(self, obj):
        prefix = '— ' if obj.parent_id else ''
        return f'{prefix}{obj.title}'


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ('photo_thumb', 'full_name', 'role_title_display', 'is_doctor', 'slug', 'is_published', 'sort_order')
    list_filter = ('is_doctor', 'role', 'is_published')
    search_fields = ('full_name', 'short_name', 'slug', 'bio')
    prepopulated_fields = {'slug': ('full_name',)}
    filter_horizontal = ('services',)
    readonly_fields = ('photo_preview', *SEO_READONLY)
    ordering = ('sort_order', 'full_name')
    list_editable = ('is_doctor',)
    list_filter_submit = True

    fieldsets = (
        (None, {
            'fields': (
                'full_name', 'short_name', 'slug', 'role', 'role_title', 'is_doctor',
                'bio', 'photo', 'photo_preview', 'services', 'legacy_path', 'sort_order',
            ),
        }),
        SEO_FIELDSET,
        ('Системне', {'classes': ('collapse',), 'fields': SEO_READONLY}),
    )

    photo_preview = admin_image_preview('photo', 'admin-preview admin-preview--lg')

    @admin.display(description='')
    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" class="admin-preview" alt="">', obj.photo.url)
        return '—'

    @admin.display(description='Посада')
    def role_title_display(self, obj):
        return obj.role_title or obj.get_role_display()


class GalleryImageInline(OrderedTabularInline):
    model = GalleryImage
    fields = ('image', 'alt_text', 'caption', 'sort_order')


@admin.register(Gallery)
class GalleryAdmin(ModelAdmin):
    inlines = [GalleryImageInline]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = SEO_READONLY
    search_fields = ('title', 'slug')

    fieldsets = (
        (None, {'fields': ('title', 'slug', 'description')}),
        SEO_FIELDSET,
        ('Системне', {'classes': ('collapse',), 'fields': SEO_READONLY}),
    )


class PriceItemInline(OrderedTabularInline):
    model = PriceItem
    fields = ('name', 'price_type', 'price', 'price_max', 'note', 'sort_order')


@admin.register(PriceList)
class PriceListAdmin(SingletonModelAdmin):
    readonly_fields = ('updated_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'currency_label', 'approval_note', 'is_published', 'updated_at'),
        }),
    )


@admin.register(PriceCategory)
class PriceCategoryAdmin(ModelAdmin):
    list_display = ('title', 'items_count', 'sort_order')
    list_filter = ('price_list',)
    search_fields = ('title',)
    inlines = [PriceItemInline]
    ordering = ('sort_order', 'title')

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial.setdefault('price_list', PriceList.load().pk)
        return initial

    @admin.display(description='Позицій')
    def items_count(self, obj):
        return obj.items.count()


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('author_name', 'rating_stars', 'is_published', 'source', 'created_at')
    list_filter = ('is_published', 'source', 'rating')
    search_fields = ('author_name', 'text')
    readonly_fields = ('created_at',)
    actions = ('publish_reviews', 'unpublish_reviews')
    date_hierarchy = 'created_at'
    list_filter_submit = True

    fieldsets = (
        (None, {'fields': ('author_name', 'text', 'rating', 'source', 'is_published', 'created_at')}),
    )

    @admin.display(description='Оцінка')
    def rating_stars(self, obj):
        if not obj.rating:
            return '—'
        return format_html('<span title="{}">{}</span>', obj.rating, '★' * obj.rating)

    @admin.action(description='Опублікувати обрані відгуки')
    def publish_reviews(self, request, queryset):
        updated = queryset.update(is_published=True)
        messages.success(request, f'Опубліковано відгуків: {updated}.')

    @admin.action(description='Приховати обрані відгуки')
    def unpublish_reviews(self, request, queryset):
        updated = queryset.update(is_published=False)
        messages.success(request, f'Приховано відгуків: {updated}.')


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(ModelAdmin):
    list_display = ('name', 'form_type', 'contact_info', 'is_processed', 'created_at')
    list_display_links = ('name',)
    list_filter = ('form_type', 'is_processed', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at',)
    actions = ('mark_processed', 'mark_unprocessed')
    date_hierarchy = 'created_at'
    list_editable = ('is_processed',)
    list_filter_submit = True

    fieldsets = (
        ('Заявка', {
            'fields': ('form_type', 'name', 'phone', 'email', 'message'),
        }),
        ('Модерація', {
            'fields': ('is_processed', 'ip_address', 'created_at'),
        }),
    )

    @admin.display(description='Контакт')
    def contact_info(self, obj):
        if obj.form_type == ContactSubmission.FORM_CALLBACK:
            return obj.phone or '—'
        return obj.email or '—'

    @admin.action(description='Позначити як оброблені')
    def mark_processed(self, request, queryset):
        updated = queryset.update(is_processed=True)
        messages.success(request, f'Оброблено заявок: {updated}.')

    @admin.action(description='Повернути в необроблені')
    def mark_unprocessed(self, request, queryset):
        updated = queryset.update(is_processed=False)
        messages.success(request, f'Повернуто в необроблені: {updated}.')


@admin.register(LegacyRedirect)
class LegacyRedirectAdmin(ModelAdmin):
    list_display = ('old_path', 'new_path', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('old_path', 'new_path')
    list_editable = ('is_active',)
    list_filter_submit = True
