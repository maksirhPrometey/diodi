"""Template tags для JSON-LD, які потребують доступу до request у includes."""

import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def breadcrumb_schema(context, crumbs):
    """BreadcrumbList JSON-LD з тієї ж структури, що рендерить includes/breadcrumbs.html."""
    request = context.get('request')
    if not crumbs or not request:
        return ''

    base_url = f'{request.scheme}://{request.get_host()}'
    items = []
    for index, item in enumerate(crumbs, start=1):
        entry = {
            '@type': 'ListItem',
            'position': index,
            'name': item.get('label', ''),
        }
        url = item.get('url')
        if url:
            entry['item'] = url if url.startswith('http') else f'{base_url}{url}'
        items.append(entry)

    data = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': items,
    }
    # payload з json.dumps() (не сирий HTML), `</` екрановано проти виходу зі <script>
    payload = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    return mark_safe(f'<script type="application/ld+json">{payload}</script>')  # nosec
