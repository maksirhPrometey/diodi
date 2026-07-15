"""Початкове наповнення CMS даними з content/legacy."""

from django.core.management.base import BaseCommand
from django.db import transaction

from src.core.models import SiteSettings, SocialLink
from src.pages.legacy_import import (
    build_legacy_redirects,
    parse_about,
    parse_contacts,
    parse_copyright_text,
    parse_gallery,
    parse_home,
    parse_laboratory,
    parse_service_tree,
    parse_services_index,
    parse_site_links,
    parse_team,
)
from src.pages.legacy_import_media import attach_image
from src.pages.legacy_import_prices import parse_prices
from src.pages.models import (
    AboutPage,
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
    TeamRole,
)

TEAM_ROLE_MAP = {
    'Головний лікар': TeamRole.CHIEF_DOCTOR,
    'Директор, провідний зубний технік': TeamRole.DIRECTOR,
    'Директор': TeamRole.DIRECTOR,
    'Лікар-стоматолог': TeamRole.DOCTOR,
    'Зубний технік': TeamRole.DENTAL_TECHNICIAN,
    'Адміністратор': TeamRole.ADMINISTRATOR,
    'Середній медперсонал': TeamRole.NURSE,
}

PRICE_TYPE_MAP = {
    'exact': PriceItem.PriceType.EXACT,
    'from': PriceItem.PriceType.FROM,
    'range': PriceItem.PriceType.RANGE,
}


class Command(BaseCommand):
    help = 'Імпортує контент з content/legacy у CMS'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Перезаписати існуючий контент')
        parser.add_argument('--dry-run', action='store_true', help='Лише показати summary без запису')
        parser.add_argument('--skip-images', action='store_true', help='Не копіювати зображення в media/')

    def handle(self, *args, **options):
        force = options['force']
        dry_run = options['dry_run']
        skip_images = options['skip_images']

        home_data = parse_home()
        about_data = parse_about()
        lab_data = parse_laboratory()
        contacts_data = parse_contacts()
        services_index_data = parse_services_index()
        services_data = parse_service_tree()
        team_data = parse_team()
        gallery_data = parse_gallery()
        prices_data = parse_prices()
        redirects = build_legacy_redirects(services_data, team_data)

        summary = {
            'services_root': len(services_data),
            'services_children': sum(len(s.get('children', [])) for s in services_data),
            'team': len(team_data),
            'gallery_images': len(gallery_data['images']),
            'price_items': sum(len(cat['items']) for cat in prices_data['categories']),
            'redirects': len(redirects),
            'home_gallery': len(home_data.get('gallery_images', [])),
        }
        self.stdout.write(f'Summary: {summary}')

        if dry_run:
            self.stdout.write(self.style.WARNING('Dry-run: запис у БД пропущено.'))
            return

        with transaction.atomic():
            self._seed_site_settings(contacts_data, skip_images, force)
            self._seed_social_links(parse_site_links(), force)
            self._seed_home(home_data, skip_images, force)
            self._seed_about(about_data, skip_images, force)
            self._seed_laboratory(lab_data, skip_images, force)
            self._seed_contacts(contacts_data, services_index_data, force)
            self._seed_services(services_data, skip_images, force)
            self._seed_team(team_data, skip_images, force)
            self._seed_gallery(gallery_data, skip_images, force)
            self._seed_prices(prices_data, force)
            self._seed_redirects(redirects, force)
            if force:
                Review.objects.all().delete()
                self._purge_orphan_redirects(redirects)

        self.stdout.write(self.style.SUCCESS('CMS seed з legacy завершено.'))

    def _should_update(self, force: bool, exists: bool) -> bool:
        return force or not exists

    def _apply_seo_fields(self, payload: dict) -> dict:
        fields = {}
        for key in ('meta_title', 'meta_description', 'og_title', 'og_description', 'canonical_url'):
            if payload.get(key):
                fields[key] = payload[key]
        return fields

    def _seed_site_settings(self, data: dict, skip_images: bool, force: bool):
        settings_obj = SiteSettings.load()
        settings_obj.phone_primary = SiteSettings.normalize_phone(data['phone_primary'])
        settings_obj.phone_secondary = SiteSettings.normalize_phone(data['phone_secondary'])
        settings_obj.email = data['email']
        settings_obj.schedule_weekdays = data['schedule_weekdays']
        settings_obj.schedule_saturday = data['schedule_saturday']
        settings_obj.schedule_sunday = data['schedule_sunday']
        settings_obj.founded_year = 2001
        settings_obj.lab_brand_name = 'Dio-Lab'
        copyright_text = parse_copyright_text()
        if copyright_text:
            settings_obj.copyright_text = copyright_text
        for key, value in self._apply_seo_fields(data).items():
            setattr(settings_obj, key, value)
        attach_image(settings_obj, 'logo', data.get('logo'), skip_images=skip_images)
        settings_obj.save()

    def _seed_social_links(self, links: list[dict], force: bool):
        settings_obj = SiteSettings.load()
        if force:
            SocialLink.objects.filter(site_settings=settings_obj).delete()
        if SocialLink.objects.filter(site_settings=settings_obj).exists() and not force:
            return
        for order, link in enumerate(links):
            SocialLink.objects.update_or_create(
                site_settings=settings_obj,
                platform=link['platform'],
                defaults={
                    'label': link['label'],
                    'url': link['url'],
                    'sort_order': order,
                },
            )

    def _seed_home(self, data: dict, skip_images: bool, force: bool):
        exists = HomePage.objects.filter(pk=1).exists()
        if not self._should_update(force, exists):
            return
        page, _ = HomePage.objects.update_or_create(
            pk=1,
            defaults={
                'hero_title': data['hero_title'],
                'intro_text': data['intro_text'],
                'benefits_title': data['benefits_title'],
                'benefits_lead': data['benefits_lead'],
                'why_us_title': data['why_us_title'],
                'why_us_text': data['why_us_text'],
                'implant_cta_text': data['implant_cta_text'],
                'implant_description': data['implant_description'],
                **self._apply_seo_fields(data),
            },
        )
        attach_image(page, 'implant_image', data.get('implant_image'), skip_images=skip_images)
        page.save()
        if force:
            HomeGalleryImage.objects.filter(home_page=page).delete()
        if force or not page.gallery_images.exists():
            for order, rel in enumerate(data.get('gallery_images', [])):
                image = HomeGalleryImage(home_page=page, sort_order=order, alt_text=rel.split('/')[-1])
                attach_image(image, 'image', rel, skip_images=skip_images)
                image.save()

    def _seed_about(self, data: dict, skip_images: bool, force: bool):
        if not self._should_update(force, AboutPage.objects.filter(pk=1).exists()):
            return
        page, _ = AboutPage.objects.update_or_create(
            pk=1,
            defaults={
                'title': data['title'],
                'body': data['body'],
                **self._apply_seo_fields(data),
            },
        )
        attach_image(page, 'image', data.get('image'), skip_images=skip_images)
        page.save()

    def _seed_laboratory(self, data: dict, skip_images: bool, force: bool):
        if not self._should_update(force, LaboratoryPage.objects.filter(pk=1).exists()):
            return
        page, _ = LaboratoryPage.objects.update_or_create(
            pk=1,
            defaults={
                'title': data['title'],
                'body': data['body'],
                **self._apply_seo_fields(data),
            },
        )
        attach_image(page, 'hero_image', data.get('hero_image'), skip_images=skip_images)
        page.save()

    def _seed_contacts(self, contacts_data: dict, services_index_data: dict, force: bool):
        if self._should_update(force, ContactsPage.objects.filter(pk=1).exists()):
            ContactsPage.objects.update_or_create(
                pk=1,
                defaults={
                    'title': contacts_data['title'],
                    'intro_text': contacts_data.get('intro_text', ''),
                    'use_site_settings': True,
                },
            )
        if self._should_update(force, ServicesIndexPage.objects.filter(pk=1).exists()):
            ServicesIndexPage.objects.update_or_create(
                pk=1,
                defaults={
                    'title': services_index_data['title'],
                    'intro_text': services_index_data['intro_text'],
                    **self._apply_seo_fields(services_index_data),
                },
            )

    def _seed_services(self, services: list[dict], skip_images: bool, force: bool):
        if Service.objects.exists() and not force:
            return
        if force:
            Service.objects.all().delete()

        for order, node in enumerate(services):
            parent = self._create_service(node, order, skip_images=skip_images)
            for child_order, child in enumerate(node.get('children', [])):
                self._create_service(child, child_order, parent=parent, skip_images=skip_images)

    def _create_service(self, node: dict, sort_order: int, parent=None, skip_images: bool = False):
        service = Service.objects.create(
            parent=parent,
            title=node['title'],
            slug=node['slug'],
            short_description=node.get('short_description', ''),
            body=node.get('body', ''),
            legacy_path=node.get('legacy_path', ''),
            is_featured=node.get('is_featured', False),
            sort_order=sort_order,
            is_published=True,
            **self._apply_seo_fields(node),
        )
        attach_image(service, 'image', node.get('image'), skip_images=skip_images)
        service.save()
        return service

    def _seed_team(self, members: list[dict], skip_images: bool, force: bool):
        if TeamMember.objects.exists() and not force:
            return
        if force:
            TeamMember.objects.all().delete()

        for member in members:
            obj = TeamMember.objects.create(
                full_name=member['full_name'],
                slug=member['slug'],
                role=TEAM_ROLE_MAP.get(member['role_title'], TeamRole.NURSE),
                role_title=member['role_title'],
                is_doctor=member.get('is_doctor', False),
                bio=member.get('bio', ''),
                legacy_path=member.get('legacy_path', ''),
                sort_order=member['sort_order'],
                is_published=True,
                **self._apply_seo_fields(member),
            )
            attach_image(obj, 'photo', member.get('photo'), skip_images=skip_images)
            obj.save()

    def _seed_gallery(self, data: dict, skip_images: bool, force: bool):
        gallery, _ = Gallery.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'title': data['title'],
                'description': data['description'],
                'is_published': True,
                **self._apply_seo_fields(data),
            },
        )
        if force:
            gallery.title = data['title']
            gallery.description = data['description']
            gallery.is_published = True
            for key, value in self._apply_seo_fields(data).items():
                setattr(gallery, key, value)
            gallery.save()
        if force:
            gallery.images.all().delete()
        if force or not gallery.images.exists():
            for order, image_data in enumerate(data['images']):
                item = GalleryImage(
                    gallery=gallery,
                    sort_order=order,
                    alt_text=image_data.get('alt_text', ''),
                )
                attach_image(item, 'image', image_data.get('path'), skip_images=skip_images)
                item.save()

    def _seed_prices(self, data: dict, force: bool):
        price_list, _ = PriceList.objects.get_or_create(
            pk=1,
            defaults={
                'title': data['title'],
                'currency_label': data['currency_label'],
                'approval_note': data.get('approval_note', ''),
                'is_published': True,
            },
        )
        if force:
            price_list.title = data['title']
            price_list.currency_label = data['currency_label']
            price_list.approval_note = data.get('approval_note', '')
            price_list.save()
            PriceCategory.objects.filter(price_list=price_list).delete()

        if PriceCategory.objects.filter(price_list=price_list).exists() and not force:
            return

        for cat_order, category in enumerate(data['categories']):
            cat = PriceCategory.objects.create(
                price_list=price_list,
                title=category['title'],
                sort_order=cat_order,
            )
            for item_order, item in enumerate(category['items']):
                PriceItem.objects.create(
                    category=cat,
                    name=item['name'],
                    price_type=PRICE_TYPE_MAP.get(item['price_type'], PriceItem.PriceType.EXACT),
                    price=item.get('price'),
                    price_max=item.get('price_max'),
                    note=item.get('note', ''),
                    sort_order=item_order,
                )

    def _seed_redirects(self, redirects: list[tuple[str, str]], force: bool):
        if force:
            LegacyRedirect.objects.all().delete()
        for old_path, new_path in redirects:
            LegacyRedirect.objects.update_or_create(
                old_path=old_path,
                defaults={'new_path': new_path, 'is_active': True},
            )

    def _purge_orphan_redirects(self, redirects: list[tuple[str, str]]):
        valid_paths = {old_path for old_path, _ in redirects}
        LegacyRedirect.objects.exclude(old_path__in=valid_paths).delete()
