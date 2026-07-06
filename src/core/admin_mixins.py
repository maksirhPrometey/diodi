from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin


class SingletonModelAdmin(ModelAdmin):
    """Admin для моделей з одним записом — одразу відкриває форму редагування."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = self.model.objects.get_or_create(pk=1)
        url = reverse(
            f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change',
            args=[obj.pk],
        )
        return HttpResponseRedirect(url)


def admin_image_preview(field_name='image', css_class='admin-preview'):
    def preview(self, obj):
        image = getattr(obj, field_name, None)
        if image:
            return format_html(
                '<img src="{}" alt="" class="{}">',
                image.url,
                css_class,
            )
        return '—'

    preview.short_description = 'Превʼю'
    return preview


SEO_FIELDSET = (
    'SEO',
    {
        'classes': ('collapse',),
        'fields': (
            'meta_title',
            'meta_description',
            'og_title',
            'og_description',
            'og_image',
            'canonical_url',
            'is_published',
        ),
    },
)

SEO_READONLY = ('created_at', 'updated_at')
