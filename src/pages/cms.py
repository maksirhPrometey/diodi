"""Читання контенту з ORM для публічних views."""

from __future__ import annotations

import json
import re

from django.db.models import Prefetch
from django.urls import reverse
from django.utils.formats import date_format
from django.utils.safestring import mark_safe

from src.pages.content_defaults import BENEFIT_ICONS, LAB_FEATURE_ICONS, SERVICE_ICONS
from src.pages.models import (
    AboutPage,
    Gallery,
    GalleryImage,
    HomeGalleryImage,
    HomePage,
    LaboratoryPage,
    PriceCategory,
    PriceItem,
    PriceList,
    Review,
    Service,
    TeamMember,
)

PRICE_CATEGORY_ICONS = ['tooth', 'activity', 'layers', 'tool']

BENEFIT_TITLES = ['Діагностика', 'Лікування', 'Профілактика']
BENEFIT_PREFIXES = ['Сучасна діагностика', 'Якісне лікування', 'Своєчасна профілактика']
LAB_FEATURE_SKIP = ('звертатись', 'провідні спеціалісти', 'запрошує', 'діоксид цирконію')


def bg_class(index):
    return f'bg-gradient-{index % 6}'


def member_initials(name):
    parts = name.split()
    return parts[0][:2] if parts else 'Д'


def split_paragraphs(text):
    if not text:
        return []
    return [part.strip() for part in text.split('\n\n') if part.strip()]


def parse_bullet_lines(text):
    if not text:
        return []
    points = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('•'):
            line = line[1:].strip()
        points.append(line)
    return points


def parse_about_sections(body):
    """Абзаци без підзаголовка — лише текст; title лише якщо є явний заголовок у блоці."""
    sections = []
    for block in split_paragraphs(body):
        lines = block.split('\n', 1)
        if len(lines) == 2 and lines[0].strip() and lines[1].strip():
            sections.append({'title': lines[0].strip(), 'text': lines[1].strip()})
        else:
            sections.append({'title': '', 'text': block})
    return sections


def service_icon(service):
    if service.parent_id:
        return SERVICE_ICONS.get(service.parent.slug, 'tooth')
    return SERVICE_ICONS.get(service.slug, 'tooth')


def format_price(item: PriceItem, currency='грн.'):
    if item.price_type == PriceItem.PriceType.FROM:
        if item.price is not None:
            return f'від {item.price:,.2f}'.replace(',', ' ').replace('.00', '.00')
        return 'від —'
    if item.price_type == PriceItem.PriceType.RANGE:
        if item.price is not None and item.price_max is not None:
            low = f'{item.price:,.2f}'.replace(',', ' ')
            high = f'{item.price_max:,.2f}'.replace(',', ' ')
            return f'{low} – {high}'
        return '—'
    if item.price is not None:
        return f'{item.price:,.2f}'.replace(',', ' ')
    return '—'


def published_services_qs():
    return (
        Service.objects.filter(is_published=True, parent__isnull=True)
        .prefetch_related(
            Prefetch(
                'children',
                queryset=Service.objects.filter(is_published=True).order_by('sort_order', 'pk'),
            ),
        )
        .order_by('sort_order', 'pk')
    )


def service_to_card(service, index=0):
    children = list(service.children.all()) if hasattr(service, '_prefetched_objects_cache') else list(
        service.children.filter(is_published=True).order_by('sort_order', 'pk'),
    )
    return {
        'slug': service.slug,
        'title': service.title,
        'desc': service.short_description,
        'icon': service_icon(service),
        'children_count': len(children),
        'bg_class': bg_class(index),
    }


def service_to_mega(service):
    children = list(service.children.all())
    return {
        'slug': service.slug,
        'title': service.title,
        'desc': service.short_description,
        'icon': service_icon(service),
        'children': [
            {'slug': child.slug, 'title': child.title}
            for child in children[:4]
        ],
    }


def service_to_detail(service, index=0):
    parent = service.parent
    if parent and not parent.is_published:
        parent = None
    children_qs = service.children.filter(is_published=True).order_by('sort_order', 'pk') if not parent else []
    children = [
        {
            'slug': child.slug,
            'title': child.title,
            'short': child.short_description,
        }
        for child in children_qs
    ]
    icon_service = parent or service
    return {
        'slug': service.slug,
        'title': service.title,
        'desc': service.short_description,
        'icon': service_icon(icon_service),
        'body': split_paragraphs(service.body),
        'children': children,
        'is_leaf': not children,
        'parent': {
            'slug': parent.slug,
            'title': parent.title,
        } if parent else None,
        'bg_class': bg_class(index),
        'image_url': service.image.url if service.image else '',
    }


def get_service_by_slug(slug):
    try:
        service = Service.objects.select_related('parent').get(slug=slug, is_published=True)
    except Service.DoesNotExist:
        return None
    root_index = 0
    if service.parent_id:
        siblings = list(
            Service.objects.filter(is_published=True, parent__isnull=True).order_by('sort_order', 'pk').values_list('slug', flat=True),
        )
        root_index = siblings.index(service.parent.slug) if service.parent.slug in siblings else 0
    else:
        siblings = list(
            Service.objects.filter(is_published=True, parent__isnull=True).order_by('sort_order', 'pk').values_list('slug', flat=True),
        )
        root_index = siblings.index(service.slug) if service.slug in siblings else 0
    return service_to_detail(service, root_index)


def team_member_to_dict(member, index=0):
    return {
        'slug': member.slug,
        'name': member.full_name,
        'role': member.role_title or member.get_role_display(),
        'is_doctor': member.is_doctor,
        'initials': member_initials(member.full_name),
        'bg_class': bg_class(index),
        'bio': split_paragraphs(member.bio),
        'photo_url': member.photo.url if member.photo else '',
        'related_services': [
            service_to_card(svc, idx)
            for idx, svc in enumerate(member.services.filter(is_published=True).order_by('sort_order', 'pk'))
        ],
    }


def media_item_to_dict(obj, index=0):
    label = getattr(obj, 'caption', None) or getattr(obj, 'alt_text', None) or f'Фото #{obj.pk}'
    return {
        'label': label,
        'bg_class': bg_class(index),
        'image_url': obj.image.url if obj.image else '',
    }


def gallery_item_to_dict(image, index=0):
    return media_item_to_dict(image, index)


def get_gallery_items(limit=None):
    gallery = (
        Gallery.objects.filter(is_published=True, slug='fotohalereia')
        .prefetch_related('images')
        .first()
    )
    if not gallery:
        return []
    images = gallery.images.all().order_by('sort_order', 'pk')
    if limit:
        images = images[:limit]
    return [media_item_to_dict(img, i) for i, img in enumerate(images)]


def get_home_gallery(limit=8):
    page = HomePage.objects.filter(is_published=True).prefetch_related('gallery_images').first()
    if page:
        images = page.gallery_images.all().order_by('sort_order', 'pk')
        if limit:
            images = images[:limit]
        if images.exists():
            return [media_item_to_dict(img, i) for i, img in enumerate(images)]
    return get_gallery_items(limit)


def home_benefits_from_intro(intro_text: str) -> list[dict]:
    if not intro_text:
        return []

    match = re.search(
        r'Сучасна діагностика, якісне лікування та своєчасна профілактика\s*[–—-]\s*(.+)',
        intro_text,
        re.IGNORECASE | re.DOTALL,
    )
    tail = match.group(1).strip().rstrip('.') if match else intro_text.strip().rstrip('.')

    return [
        {
            'title': BENEFIT_TITLES[index],
            'text': f'{BENEFIT_PREFIXES[index]} — {tail}.',
            'icon': BENEFIT_ICONS[index],
        }
        for index in range(3)
    ]


def lab_features_from_body(body: str) -> list[dict]:
    paragraphs = [paragraph.strip() for paragraph in body.split('\n\n') if paragraph.strip()]
    items = []
    for paragraph in paragraphs:
        lowered = paragraph.lower()
        if any(fragment in lowered for fragment in LAB_FEATURE_SKIP):
            continue
        items.append(paragraph)
        if len(items) >= 3:
            break

    features = []
    for index, paragraph in enumerate(items):
        sentence = paragraph.split('. ')[0].strip()
        title = sentence if len(sentence) <= 80 else f'{sentence[:77]}…'
        features.append({
            'title': title.rstrip('.'),
            'text': paragraph,
            'icon': LAB_FEATURE_ICONS[index % len(LAB_FEATURE_ICONS)],
        })
    return features


def pick_hero_image_url(gallery_items):
    """Hero — фото 3D сканування (перший банер з legacy головної)."""
    if not gallery_items:
        return ''

    for item in gallery_items:
        label = item.get('label') or ''
        url = item.get('image_url', '')
        if '5507' in label or '5507' in url:
            return url

    return gallery_items[0].get('image_url', '')


def hero_lead_text(home_page):
    if not home_page or not home_page.intro_text:
        return ''
    text = ' '.join(home_page.intro_text.split())
    if len(text) <= 200:
        return text
    chunk = text[:220]
    stop = max(chunk.rfind('.'), chunk.rfind('!'), chunk.rfind('?'))
    if stop > 80:
        return text[: stop + 1]
    return chunk.rsplit(' ', 1)[0] + '…'


def get_price_categories():
    price_list = PriceList.objects.filter(is_published=True).first()
    if not price_list:
        return [], None
    categories = (
        PriceCategory.objects.filter(price_list=price_list)
        .prefetch_related('items')
        .order_by('sort_order', 'pk')
    )
    result = []
    for index, category in enumerate(categories):
        result.append({
            'title': category.title,
            'icon': PRICE_CATEGORY_ICONS[index % len(PRICE_CATEGORY_ICONS)],
            'items': [
                {
                    'name': item.name,
                    'price': format_price(item, price_list.currency_label),
                }
                for item in category.items.all().order_by('sort_order', 'pk')
            ],
        })
    return result, price_list


def get_reviews():
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')
    return [
        {
            'author': review.author_name,
            'date': date_format(review.created_at, 'F Y'),
            'stars': review.rating or 5,
            'text': review.text,
            'initial': review.author_name[0],
            'bg_class': bg_class(index),
            'star_list': list(range(review.rating or 5)),
        }
        for index, review in enumerate(reviews)
    ]


def seo_context(obj):
    if not obj:
        return {}
    title = getattr(obj, 'meta_title', '') or getattr(obj, 'title', '') or getattr(obj, 'hero_title', '')
    description = getattr(obj, 'meta_description', '') or ''
    og_image = getattr(obj, 'og_image', None)
    return {
        'meta_title': title,
        'meta_description': description,
        'og_title': getattr(obj, 'og_title', '') or title,
        'og_description': getattr(obj, 'og_description', '') or description,
        'og_image_url': og_image.url if og_image else '',
    }


def build_ld_json(data):
    """JSON-LD payload, безпечний для вставки в <script type="application/ld+json">."""
    if not data:
        return ''
    # payload з json.dumps() (не сирий HTML), `</` екрановано проти виходу зі <script>
    payload = json.dumps(data, ensure_ascii=False)
    return mark_safe(payload.replace('</', '<\\/'))  # nosec


def dentist_schema(request, settings_obj):
    """LocalBusiness/Dentist JSON-LD з NAP-даних SiteSettings (глобально, у footer)."""
    base_url = f'{request.scheme}://{request.get_host()}'
    data = {
        '@context': 'https://schema.org',
        '@type': 'Dentist',
        'name': settings_obj.site_name,
        'url': f'{base_url}/',
    }
    if settings_obj.phone_primary:
        data['telephone'] = settings_obj.phone_primary_display
    if settings_obj.email:
        data['email'] = settings_obj.email
    if settings_obj.address:
        data['address'] = {
            '@type': 'PostalAddress',
            'streetAddress': settings_obj.address,
            'addressLocality': 'Івано-Франківськ',
            'addressCountry': 'UA',
        }
    if settings_obj.latitude and settings_obj.longitude:
        data['geo'] = {
            '@type': 'GeoCoordinates',
            'latitude': float(settings_obj.latitude),
            'longitude': float(settings_obj.longitude),
        }
    if settings_obj.logo:
        data['image'] = base_url + settings_obj.logo.url
    return data


def website_schema(request):
    base_url = f'{request.scheme}://{request.get_host()}'
    return {
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        'name': 'Стоматологія «ДіОДі»',
        'url': f'{base_url}/',
    }


def service_ld_data(request, service_data):
    base_url = f'{request.scheme}://{request.get_host()}'
    data = {
        '@context': 'https://schema.org',
        '@type': 'Service',
        'name': service_data.get('title', ''),
        'description': service_data.get('desc', ''),
        'url': base_url + reverse('service_detail', args=[service_data['slug']]),
        'provider': {
            '@type': 'Dentist',
            'name': 'Стоматологія «ДіОДі»',
        },
        'areaServed': 'Івано-Франківськ',
    }
    image_url = service_data.get('image_url')
    if image_url:
        data['image'] = image_url if image_url.startswith('http') else base_url + image_url
    return data


def person_ld_data(request, member_data):
    base_url = f'{request.scheme}://{request.get_host()}'
    data = {
        '@context': 'https://schema.org',
        '@type': 'Person',
        'name': member_data.get('name', ''),
        'jobTitle': member_data.get('role', ''),
        'url': base_url + reverse('team_member', args=[member_data['slug']]),
        'worksFor': {
            '@type': 'Dentist',
            'name': 'Стоматологія «ДіОДі»',
        },
    }
    photo_url = member_data.get('photo_url')
    if photo_url:
        data['image'] = photo_url if photo_url.startswith('http') else base_url + photo_url
    return data
