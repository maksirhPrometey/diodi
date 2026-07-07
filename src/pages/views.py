import logging

from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from django.urls import reverse

from src.core.models import SiteSettings
from src.pages.cms import (
    build_ld_json,
    get_gallery_items,
    get_home_gallery,
    get_price_categories,
    get_reviews,
    get_service_by_slug,
    hero_lead_text,
    lab_features_from_body,
    parse_about_sections,
    parse_bullet_lines,
    person_ld_data,
    pick_hero_image_url,
    published_services_qs,
    seo_context,
    service_ld_data,
    service_to_card,
    split_paragraphs,
    team_member_to_dict,
    website_schema,
)
from src.pages.forms import ContactForm
from src.pages.models import (
    AboutPage,
    ContactSubmission,
    ContactsPage,
    Gallery,
    HomePage,
    LaboratoryPage,
    Service,
    ServicesIndexPage,
    TeamMember,
)
from src.pages.security import is_rate_limited, verify_recaptcha

logger = logging.getLogger(__name__)


def _nav_context(active):
    return {'nav_active': active}


def _crumbs(*items):
    trail = [{'label': 'Головна', 'url': reverse('home')}]
    for label, url in items:
        if url:
            trail.append({'label': label, 'url': url})
        else:
            trail.append({'label': label})
    return trail


def _published_or_404(model, pk=1):
    obj = get_object_or_404(model, pk=pk)
    if hasattr(obj, 'is_published') and not obj.is_published:
        raise Http404()
    return obj


def home_view(request):
    home_page = HomePage.objects.filter(is_published=True).prefetch_related('gallery_images').first()
    root_services = list(published_services_qs())
    team_qs = TeamMember.objects.filter(is_published=True).order_by('sort_order', 'pk')[:4]
    home_gallery = get_home_gallery(8)
    scan_service = Service.objects.filter(slug='3d-skanuvannya', is_published=True).first()
    services_index = ServicesIndexPage.objects.filter(is_published=True).first()
    gallery_page = Gallery.objects.filter(is_published=True, slug='fotohalereia').first()

    context = {
        **_nav_context('home'),
        **seo_context(home_page),
        'home_page': home_page,
        'why_points': parse_bullet_lines(home_page.why_us_text) if home_page else [],
        'services': [service_to_card(s, i) for i, s in enumerate(root_services)],
        'services_intro': services_index.intro_text if services_index else '',
        'gallery_intro': gallery_page.description if gallery_page else '',
        'team_teaser': [
            {
                'slug': m.slug,
                'name': m.full_name,
                'role': m.role_title or m.get_role_display(),
                'photo_url': m.photo.url if m.photo else '',
            }
            for m in team_qs
        ],
        'home_gallery': home_gallery,
        'hero_image_url': pick_hero_image_url(home_gallery),
        'hero_lead': hero_lead_text(home_page),
        'why_image_url': scan_service.image.url if scan_service and scan_service.image else '',
        'team_count': TeamMember.objects.filter(is_published=True).count(),
        'callback_form': ContactForm(form_type=ContactSubmission.FORM_CALLBACK),
        'email_form': ContactForm(form_type=ContactSubmission.FORM_EMAIL),
        'schema_json': build_ld_json(website_schema(request)),
    }
    return render(request, 'pages/home.html', context)


def about_view(request):
    about_page = _published_or_404(AboutPage)
    context = {
        **_nav_context('about'),
        **seo_context(about_page),
        'about_page': about_page,
        'sections': parse_about_sections(about_page.body),
        'breadcrumbs': _crumbs(('Про клініку', None)),
    }
    return render(request, 'pages/about.html', context)


def team_list_view(request):
    members = TeamMember.objects.filter(is_published=True).order_by('sort_order', 'pk')
    context = {
        **_nav_context('team'),
        'team': [team_member_to_dict(m, i) for i, m in enumerate(members)],
        'breadcrumbs': _crumbs(('Про нас', reverse('about')), ('Наша команда', None)),
    }
    return render(request, 'pages/team.html', context)


def team_member_view(request, slug):
    member = get_object_or_404(TeamMember, slug=slug, is_published=True)
    members = list(TeamMember.objects.filter(is_published=True).order_by('sort_order', 'pk'))
    index = next((i for i, m in enumerate(members) if m.pk == member.pk), 0)
    context = {
        **_nav_context('team'),
        **seo_context(member),
        'member': team_member_to_dict(member, index),
        'breadcrumbs': _crumbs(
            ('Про нас', reverse('about')),
            ('Команда', reverse('team')),
            (member.full_name, None),
        ),
        'schema_json': build_ld_json(person_ld_data(request, team_member_to_dict(member, index))),
    }
    return render(request, 'pages/team_member.html', context)


def gallery_view(request):
    from src.pages.models import Gallery
    gallery = Gallery.objects.filter(is_published=True, slug='fotohalereia').first()
    context = {
        **_nav_context('gallery'),
        **seo_context(gallery),
        'gallery_page': gallery,
        'gallery': get_gallery_items(),
        'breadcrumbs': _crumbs(('Про нас', reverse('about')), ('Фотогалерея', None)),
    }
    return render(request, 'pages/gallery.html', context)


def services_view(request):
    index_page = ServicesIndexPage.objects.filter(is_published=True).first()
    root_services = list(published_services_qs())
    context = {
        **_nav_context('services'),
        **seo_context(index_page),
        'services_page': index_page,
        'services': [service_to_card(s, i) for i, s in enumerate(root_services)],
        'breadcrumbs': _crumbs(('Послуги', None)),
    }
    return render(request, 'pages/services.html', context)


def service_detail_view(request, slug):
    service_data = get_service_by_slug(slug)
    if not service_data:
        return redirect('services')
    service = get_object_or_404(Service, slug=slug, is_published=True)
    parent = service_data.get('parent')
    if parent:
        crumbs = _crumbs(
            ('Послуги', reverse('services')),
            (parent['title'], reverse('service_detail', args=[parent['slug']])),
            (service_data['title'], None),
        )
    else:
        crumbs = _crumbs(('Послуги', reverse('services')), (service_data['title'], None))
    other_services = [
        service_to_card(s, i)
        for i, s in enumerate(published_services_qs())
        if s.slug != (parent['slug'] if parent else service.slug)
    ]
    context = {
        **_nav_context('services'),
        **seo_context(service),
        'service': service_data,
        'other_services': other_services,
        'breadcrumbs': crumbs,
        'schema_json': build_ld_json(service_ld_data(request, service_data)),
    }
    return render(request, 'pages/service_detail.html', context)


def laboratory_view(request):
    lab_page = _published_or_404(LaboratoryPage)
    lab_paragraphs = split_paragraphs(lab_page.body)
    lab_cta_candidates = [
        paragraph for paragraph in lab_paragraphs
        if any(fragment in paragraph.lower() for fragment in ('запрошує', 'звертатись'))
    ]
    context = {
        **_nav_context('lab'),
        **seo_context(lab_page),
        'lab_page': lab_page,
        'lab_features': lab_features_from_body(lab_page.body),
        'lab_body': lab_paragraphs[:2],
        'lab_cta_text': lab_cta_candidates[0] if lab_cta_candidates else '',
        'lab_gallery': get_gallery_items(4),
        'breadcrumbs': _crumbs(('Лабораторія Dio-Lab', None)),
    }
    return render(request, 'pages/laboratory.html', context)


def prices_view(request):
    price_categories, price_list = get_price_categories()
    context = {
        **_nav_context('prices'),
        'price_categories': price_categories,
        'price_list': price_list,
        'breadcrumbs': _crumbs(('Ціни', None)),
    }
    return render(request, 'pages/prices.html', context)


def reviews_view(request):
    context = {
        **_nav_context('reviews'),
        'reviews': get_reviews(),
        'breadcrumbs': _crumbs(('Відгуки', None)),
    }
    return render(request, 'pages/reviews.html', context)


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _handle_contact_post(request, form_type):
    ip_address = _client_ip(request)
    form = ContactForm(request.POST, form_type=form_type)
    rate_limited = is_rate_limited(ip_address)

    if rate_limited:
        form.add_error(None, 'Забагато спроб. Спробуйте, будь ласка, через хвилину.')
    elif not verify_recaptcha(request):
        form.add_error(None, 'Підтвердіть, будь ласка, що ви не робот.')
    elif form.is_valid():
        submission = form.save(commit=False)
        submission.ip_address = ip_address
        submission.save()
        recipient = SiteSettings.load().email
        try:
            send_mail(
                subject=f'Заявка з сайту ДіОДі ({submission.get_form_type_display()})',
                message=(
                    f"Ім'я: {submission.name}\n"
                    f"Телефон: {submission.phone or '—'}\n"
                    f"Email: {submission.email or '—'}\n"
                    f"Повідомлення:\n{submission.message}"
                ),
                from_email=None,
                recipient_list=[recipient],
                fail_silently=False,
            )
        except Exception:
            logger.exception('Не вдалося надіслати email-сповіщення про заявку #%s', submission.pk)
        if request.headers.get('HX-Request'):
            form_id = 'form-callback' if form_type == ContactSubmission.FORM_CALLBACK else 'form-email'
            form_variant = 'callback' if form_type == ContactSubmission.FORM_CALLBACK else 'email'
            return render(request, 'includes/contact_form_success.html', {
                'form_id': form_id,
                'form_variant': form_variant,
            })
        messages.success(request, 'Дякуємо! Ми звʼяжемося з вами найближчим часом.')
        return redirect('contacts')

    status = 429 if rate_limited else 422
    if request.headers.get('HX-Request'):
        template = (
            'includes/contact_form_callback.html'
            if form_type == ContactSubmission.FORM_CALLBACK
            else 'includes/contact_form_email.html'
        )
        return render(request, template, {'form': form}, status=status)
    return None


@require_http_methods(['GET', 'POST'])
def contacts_view(request):
    contacts_page = ContactsPage.objects.filter(is_published=True).first()
    callback_form = ContactForm(form_type=ContactSubmission.FORM_CALLBACK)
    email_form = ContactForm(form_type=ContactSubmission.FORM_EMAIL)

    if request.method == 'POST':
        form_type = request.POST.get('form_type', ContactSubmission.FORM_CALLBACK)
        response = _handle_contact_post(request, form_type)
        if response:
            return response
        callback_form = ContactForm(request.POST, form_type=ContactSubmission.FORM_CALLBACK)
        email_form = ContactForm(request.POST, form_type=ContactSubmission.FORM_EMAIL)

    context = {
        **_nav_context('contacts'),
        **seo_context(contacts_page),
        'contacts_page': contacts_page,
        'callback_form': callback_form,
        'email_form': email_form,
        'breadcrumbs': _crumbs(('Контакти', None)),
    }
    return render(request, 'pages/contacts.html', context)


def contact_form_partial_view(request, variant):
    if request.method == 'POST':
        form_type = ContactSubmission.FORM_CALLBACK if variant == 'callback' else ContactSubmission.FORM_EMAIL
        response = _handle_contact_post(request, form_type)
        if response:
            return response
    form = ContactForm(
        form_type=ContactSubmission.FORM_CALLBACK if variant == 'callback' else ContactSubmission.FORM_EMAIL,
    )
    template = (
        'includes/contact_form_callback.html'
        if variant == 'callback'
        else 'includes/contact_form_email.html'
    )
    return render(request, template, {'form': form})
