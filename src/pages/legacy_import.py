"""Імпорт контенту з content/legacy у структури для CMS."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from src.core.models import SiteSettings
from src.pages.legacy_import_media import image_rel_from_markdown, image_rel_from_url

LEGACY_ROOT = Path(__file__).resolve().parent.parent.parent / 'content' / 'legacy'
TEXT_DIR = LEGACY_ROOT / 'text'
INDEX_PATH = TEXT_DIR / 'index.json'

SERVICE_TREE = [
    {
        'slug': 'terapevtychna-stomatolohiia',
        'file': 'posluhy/terapevtychna-stomatolohiia.md',
        'children': [
            {'slug': 'estetychna-restavratsiia', 'file': 'posluhy/estetychna-restavratsiia.md'},
            {'slug': 'endodontiia', 'file': 'posluhy/endodontiia.md'},
            {'slug': 'profesiina-hihiiena', 'file': 'posluhy/profesiina-hihiiena.md'},
            {'slug': 'plombuvannia', 'file': 'posluhy/plombuvannia.md'},
            {'slug': 'profesiine-vidbiliuvannia', 'file': 'posluhy/profesiine-vidbiliuvannia.md'},
            {'slug': 'likuvannia-paradontu', 'file': 'posluhy/likuvannia-paradontu.md'},
        ],
    },
    {
        'slug': 'ortopedychna-stomatolohiia',
        'file': 'posluhy/ortopedychna-stomatolohiia.md',
        'children': [
            {'slug': 'neznimne-protezuvannia', 'file': 'posluhy/neznimne-protezuvannia.md'},
            {'slug': 'znimne-protezuvannia', 'file': 'posluhy/znimne-protezuvannia.md'},
        ],
    },
    {'slug': 'khirurhiia', 'file': 'posluhy/khirurhiia.md'},
    {'slug': 'implantolohiia', 'file': 'posluhy/implantolohiia.md'},
    {'slug': 'renthenohrafiia', 'file': 'posluhy/renthenohrafiia.md'},
    {'slug': '3d-skanuvannya', 'file': 'posluhy/3d-skanuvannya.md'},
]

TEAM_DIR = TEXT_DIR / 'team'

TEAM_SLUG_BY_FILE = {
    'holovnyi-likar.md': 'labiy',
    'dyrektor.md': 'dzhus-oleh',
    'likar-skovorodniev.md': 'skovorodnev',
    'moderuk.md': 'maderuk',
    'administrator.md': 'dzhus-olena',
    'basarab.md': 'basarab',
    'volochii.md': 'volochiy',
}

TEAM_DOCTOR_SLUGS = {'labiy', 'skovorodnev'}

TEAM_ROLE_PREFIXES = (
    'Директор, провідний зубний технік',
    'Cередній медичний персонал',
    'Середній медичний персонал',
    'Головний лікар',
    'Лікар-стоматолог',
    'Зубний технік',
    'Адміністратор',
)

MANUAL_REDIRECTS = [
    (
        '/pro-nas/nasha-komanda/cerednii-medychnyi-personal-petrushka-snizhana-serhiivna',
        '/pro-nas/nasha-komanda/basarab/',
    ),
    (
        '/pro-nas/nasha-komanda/likar-stomatoloh-dubishchak-vitaliia-yakivna',
        '/pro-nas/nasha-komanda/',
    ),
    (
        '/pro-nas/nasha-komanda/cerednii-medychnyi-personal-dutchak-halyna-mykolaivna',
        '/pro-nas/nasha-komanda/',
    ),
    (
        '/pro-nas/nasha-komanda/holovnyi-likar',
        '/pro-nas/nasha-komanda/labiy/',
    ),
    (
        '/pro-nas/nasha-komanda/dyrektor',
        '/pro-nas/nasha-komanda/dzhus-oleh/',
    ),
    (
        '/pro-nas/nasha-komanda/likar-skovorodniev',
        '/pro-nas/nasha-komanda/skovorodnev/',
    ),
    (
        '/pro-nas/nasha-komanda/administrator-platonova-olena',
        '/pro-nas/nasha-komanda/dzhus-olena/',
    ),
    (
        '/pro-nas/nasha-komanda/zubnyi-tekhnik-moderuk',
        '/pro-nas/nasha-komanda/maderuk/',
    ),
    (
        '/pro-nas/nasha-komanda/molodshyi-medychnyi-personal-svintsytska-nataliia-valeriivna',
        '/pro-nas/nasha-komanda/',
    ),
    (
        '/pro-nas/nasha-komanda/cerednii-medychnyi-personal-volochii-ivanna-serhiivna',
        '/pro-nas/nasha-komanda/volochiy/',
    ),
]

SITE_SOCIAL_LINKS = [
    {
        'platform': 'instagram',
        'label': 'Instagram',
        'url': 'https://www.instagram.com/clinicdiodi',
    },
    {
        'platform': 'facebook',
        'label': 'Facebook',
        'url': 'https://www.facebook.com/profile.php?id=100063695671216',
    },
]

EXTERNAL_RESOURCE_LINKS = [
    {
        'platform': 'external',
        'label': 'Лазерна епіляція',
        'url': 'https://dio-lazer.if.ua/',
    },
]

IMAGE_MD = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
FRONTMATTER_SPLIT = re.compile(r'^---\s*$', re.M)


@dataclass
class MarkdownDoc:
    meta: dict
    body: str
    headings: list[dict] = field(default_factory=list)
    paragraphs: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)


def load_index() -> dict:
    return json.loads(INDEX_PATH.read_text(encoding='utf-8'))


def seo_by_path(path: str) -> dict:
    data = load_index()
    normalized = path if path != '/' else '/'
    for entry in data.get('pages', []):
        if entry.get('path') == normalized:
            return parse_seo(entry)
    return {}


def seo_by_file(file_path: str) -> dict:
    data = load_index()
    for entry in data.get('pages', []):
        if entry.get('file') == file_path:
            return parse_seo(entry)
    return {}


def parse_seo(entry: dict) -> dict:
    seo = entry.get('seo') or {}
    og_image = seo.get('og_image') or ''
    return {
        'meta_title': seo.get('title', '')[:70],
        'meta_description': seo.get('description', '')[:160],
        'og_title': seo.get('og_title', '')[:70],
        'og_description': seo.get('og_description', '')[:200],
        'canonical_url': seo.get('canonical', ''),
        'og_image_rel': image_rel_from_url(og_image),
    }


def load_markdown(relative_path: str) -> MarkdownDoc:
    raw = (TEXT_DIR / relative_path).read_text(encoding='utf-8')
    parts = FRONTMATTER_SPLIT.split(raw.strip(), maxsplit=2)
    if len(parts) < 3:
        return MarkdownDoc(meta={}, body=raw, paragraphs=[], headings=[], images=[])

    meta_lines = [line for line in parts[1].strip().splitlines() if ':' in line]
    meta = {}
    for line in meta_lines:
        key, value = line.split(':', 1)
        meta[key.strip()] = value.strip()

    body = parts[2].strip()
    main_body, image_block = split_main_body(body)
    images = IMAGE_MD.findall(image_block or '')
    images = [image_rel_from_markdown(path) for path in images]

    headings = []
    paragraphs = []
    for line in main_body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('#'):
            level = len(stripped) - len(stripped.lstrip('#'))
            text = stripped.lstrip('#').strip()
            headings.append({'level': level, 'text': text})
        elif not stripped.startswith('|'):
            paragraphs.append(stripped)

    return MarkdownDoc(
        meta=meta,
        body=main_body,
        headings=headings,
        paragraphs=paragraphs,
        images=images,
    )


def split_main_body(body: str) -> tuple[str, str]:
    marker = '## Зображення'
    if marker in body:
        main, images = body.split(marker, 1)
        return main.strip(), images.strip()
    return body.strip(), ''


def paragraphs_text(doc: MarkdownDoc) -> str:
    return '\n\n'.join(doc.paragraphs)


def first_paragraph(doc: MarkdownDoc) -> str:
    return doc.paragraphs[0] if doc.paragraphs else ''


def first_sentence(text: str) -> str:
    normalized = ' '.join(text.split())
    for sep in ('. ', '! ', '? '):
        idx = normalized.find(sep)
        if idx != -1:
            return normalized[: idx + 1].strip()
    return normalized.strip()


def split_benefits_lead(paragraph: str) -> tuple[str, str]:
    if not paragraph:
        return '', ''
    title = first_sentence(paragraph)
    lead = paragraph[len(title):].strip()
    return title, lead


def parse_home() -> dict:
    doc = load_markdown('home.md')
    seo = seo_by_path('/')
    hero_title = next((h['text'] for h in doc.headings if h['level'] == 1), doc.meta.get('title', ''))

    implant_idx = next(
        (i for i, paragraph in enumerate(doc.paragraphs) if 'імплантація' in paragraph.lower()),
        len(doc.paragraphs),
    )
    intro_paras = doc.paragraphs[:implant_idx]
    implant_paras = doc.paragraphs[implant_idx:]

    intro_text = intro_paras[0] if intro_paras else ''
    benefits_source = intro_paras[1] if len(intro_paras) > 1 else ''
    why_text = intro_paras[2] if len(intro_paras) > 2 else ''
    benefits_title, benefits_lead = split_benefits_lead(benefits_source)
    why_title = next(
        (heading['text'] for heading in doc.headings if heading['level'] == 3),
        'Чому обирають нас?',
    )

    return {
        'hero_title': hero_title,
        'intro_text': intro_text,
        'benefits_title': benefits_title,
        'benefits_lead': benefits_lead,
        'why_us_title': why_title,
        'why_us_text': why_text,
        'implant_cta_text': 'Імплантологія',
        'implant_description': '\n\n'.join(implant_paras),
        'gallery_images': dedupe_gallery_images(doc.images),
        'hero_image': pick_legacy_hero_image(doc.images),
        'implant_image': 'poslugi/implantaciya.jpg' if 'poslugi/implantaciya.jpg' in doc.images else (doc.images[-1] if doc.images else None),
        **seo,
    }


# IMG_5508 — той самий рекламний кадр «3D сканування», що й IMG_5507
# (використовується як hero), тому в сітці галереї він зайвий дубль.
DUPLICATE_GALLERY_MARKERS = ('5508',)


def dedupe_gallery_images(images: list[str]) -> list[str]:
    return [path for path in images if not any(marker in path for marker in DUPLICATE_GALLERY_MARKERS)]


def pick_legacy_hero_image(images: list[str]) -> str | None:
    for path in images:
        if '5507' in path:
            return path
    for path in images:
        if 'glavnaya/' in path:
            return path
    return images[0] if images else None


def parse_about() -> dict:
    doc = load_markdown('pro-nas.md')
    seo = seo_by_path('/pro-nas')
    title = next((h['text'] for h in doc.headings if h['level'] == 1), 'Про клініку «ДіОДі»')
    return {
        'title': title.rstrip('.'),
        'body': paragraphs_text(doc),
        'image': doc.images[0] if doc.images else None,
        **seo,
    }


def parse_laboratory() -> dict:
    doc = load_markdown('labaratoriia.md')
    seo = seo_by_path('/labaratoriia')
    title = next((h['text'] for h in doc.headings if h['level'] == 1), 'Лабораторія Dio-Lab')
    return {
        'title': title,
        'body': paragraphs_text(doc),
        'hero_image': doc.images[0] if doc.images else None,
        **seo,
    }


def _pick_phone(phones: list[str], digits_prefix: str, fallback: str) -> str:
    for raw in phones:
        normalized = SiteSettings.normalize_phone(raw)
        if ''.join(ch for ch in normalized if ch.isdigit()).startswith(digits_prefix):
            return normalized
    return fallback


def parse_contacts() -> dict:
    doc = load_markdown('kontakty.md')
    seo = seo_by_path('/kontakty')
    phones = re.findall(r'\+38\s*\(\d{3}\)\s*[\d-]+', doc.body)
    email_match = re.search(r'[\w.+-]+@[\w.-]+\.\w+', doc.body)
    schedule = {'weekdays': '', 'saturday': '', 'sunday': ''}
    for line in doc.body.splitlines():
        if 'Пн' in line and 'Пт' in line:
            schedule['weekdays'] = line.split('|')[-1].strip() if '|' in line else '9:30 – 21:00'
        if 'Суб' in line:
            schedule['saturday'] = line.split('|')[-1].strip() if '|' in line else 'за записом'
        if 'Нед' in line:
            schedule['sunday'] = line.split('|')[-1].strip() if '|' in line else 'вихідний'
    # 067 — основний номер (усі месенджери), 050 — додатковий.
    return {
        'title': next((h['text'] for h in doc.headings if h['level'] == 1), 'Контакти'),
        'intro_text': '',
        'phone_primary': _pick_phone(phones, '067', '(067) 343-60-10'),
        'phone_secondary': _pick_phone(phones, '050', '(050) 537-76-57'),
        'email': email_match.group(0) if email_match else 'diodi2001@gmail.com',
        'schedule_weekdays': schedule['weekdays'] or '9:30 – 21:00',
        'schedule_saturday': schedule['saturday'] or 'за записом',
        'schedule_sunday': schedule['sunday'] or 'вихідний',
        'logo': 'logo.jpg',
        **seo,
    }


def parse_services_index() -> dict:
    doc = load_markdown('posluhy.md')
    seo = seo_by_path('/posluhy')
    return {
        'title': 'Послуги',
        'intro_text': paragraphs_text(doc),
        **seo,
    }


def _service_payload(node: dict) -> dict:
    doc = load_markdown(node['file'])
    source_url = doc.meta.get('source_url', '')
    legacy_path = urlparse(source_url).path if source_url else ''
    title = next((h['text'] for h in doc.headings if h['level'] == 1), doc.meta.get('title', node['slug']))
    short = doc.paragraphs[0] if doc.paragraphs else ''
    if len(short) > 300:
        short = short[:297] + '…'
    seo = seo_by_file(node['file'])
    return {
        'slug': node['slug'],
        'title': title.rstrip('.'),
        'short_description': short,
        'body': paragraphs_text(doc),
        'image': doc.images[0] if doc.images else seo.get('og_image_rel'),
        'legacy_path': legacy_path,
        'is_featured': False,
        'children': [_service_payload(child) for child in node.get('children', [])],
        **seo,
    }


def parse_service_tree() -> list[dict]:
    return [_service_payload(node) for node in SERVICE_TREE]


def _team_roster_order() -> list[str]:
    doc = load_markdown('team/nasha-komanda.md')
    return [
        heading['text']
        for heading in doc.headings
        if heading['level'] == 3 and len(heading['text'].split()) >= 3
    ]


def _team_roster_images() -> list[str]:
    return load_markdown('team/nasha-komanda.md').images


def _split_role_name(title: str) -> tuple[str, str]:
    cleaned = title.strip()
    for role in TEAM_ROLE_PREFIXES:
        if cleaned.lower().startswith(role.lower()):
            return role, cleaned[len(role):].strip(' ,.')
    parts = cleaned.split()
    if len(parts) >= 4:
        return ' '.join(parts[:-3]), ' '.join(parts[-3:])
    return '', cleaned


def _team_photo_for_name(full_name: str, doc_images: list[str], roster_images: list[str]) -> str | None:
    if doc_images:
        return doc_images[0]

    lowered_name = full_name.lower()
    surname = full_name.split()[0].lower()
    if surname == 'джус':
        patterns = ('jus-olena', 'olena') if 'олена' in lowered_name else ('jus-oleg', 'oleg')
    elif surname == 'басараб':
        patterns = ('irina', 'ірина', 'basarab')
    elif surname == 'сковороднєв':
        patterns = ('skovorodnev',)
    elif surname == 'мадерук':
        patterns = ('maderuk',)
    elif surname == 'свінціцка':
        patterns = ('svincicka',)
    elif surname == 'волочій':
        patterns = ('volociy', 'voloch')
    elif surname == 'лабій':
        patterns = ('labiy',)
    else:
        patterns = (surname[:5],)

    for rel in roster_images:
        rel_lower = rel.lower()
        if any(pattern in rel_lower for pattern in patterns):
            return rel
    return None


def _team_files_from_index() -> list[dict]:
    entries = []
    for page in load_index().get('pages', []):
        file_path = page.get('file', '')
        if not file_path.startswith('team/') or file_path == 'team/nasha-komanda.md':
            continue
        if page.get('status') != 'ok':
            continue
        entries.append(page)
    return entries


def parse_team() -> list[dict]:
    roster_order = _team_roster_order()
    roster_images = _team_roster_images()
    members = []

    for entry in _team_files_from_index():
        file_name = Path(entry['file']).name
        slug = TEAM_SLUG_BY_FILE.get(file_name)
        if not slug:
            continue

        doc = load_markdown(entry['file'])
        title = next((heading['text'] for heading in doc.headings if heading['level'] == 1), doc.meta.get('title', ''))
        role_title, full_name = _split_role_name(title)
        legacy_path = urlparse(doc.meta.get('source_url', '')).path or entry.get('path', '')
        seo = seo_by_file(entry['file'])
        members.append({
            'slug': slug,
            'full_name': full_name,
            'role_title': role_title,
            'is_doctor': slug in TEAM_DOCTOR_SLUGS,
            'bio': paragraphs_text(doc),
            'photo': _team_photo_for_name(full_name, doc.images, roster_images),
            'legacy_path': legacy_path,
            'sort_order': roster_order.index(full_name) if full_name in roster_order else len(members),
            **seo,
        })

    members.sort(key=lambda item: item['sort_order'])
    for order, member in enumerate(members):
        member['sort_order'] = order
    return members


def parse_gallery() -> dict:
    doc = load_markdown('fotohalereia.md')
    seo = seo_by_path('/pro-nas/fotohalereia')
    return {
        'title': next((h['text'] for h in doc.headings if h['level'] == 1), 'Фотогалерея'),
        'description': seo.get('meta_description', ''),
        'slug': 'fotohalereia',
        'images': [{'path': rel, 'alt_text': Path(rel).stem} for rel in doc.images],
        **seo,
    }


def parse_copyright_text() -> str:
    doc = load_markdown('vidhuky.md')
    for paragraph in doc.paragraphs:
        if 'copyright' in paragraph.lower():
            return paragraph
    return ''


def parse_site_links() -> list[dict]:
    return [*SITE_SOCIAL_LINKS, *EXTERNAL_RESOURCE_LINKS]


def build_legacy_redirects(services: list[dict], team: list[dict]) -> list[tuple[str, str]]:
    redirects = {old: new for old, new in MANUAL_REDIRECTS}

    for member in team:
        old = member.get('legacy_path')
        new = f"/pro-nas/nasha-komanda/{member['slug']}/"
        if old and old.rstrip('/') != new.rstrip('/'):
            redirects[old.rstrip('/')] = new

    def walk_service_nodes(nodes: list[dict]):
        for node in nodes:
            old = node.get('legacy_path', '').rstrip('/')
            new = f"/posluhy/{node['slug']}/"
            if old and old != new.rstrip('/'):
                redirects[old] = new
            walk_service_nodes(node.get('children', []))

    walk_service_nodes(services)
    return sorted(redirects.items())
