"""Парсер прейскуранту з content/legacy/text/tsiny.md."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation

from src.pages.legacy_import import load_markdown

PRICE_CATEGORY_TITLES = [
    'Терапевтичні роботи',
    'Лікування каналів',
    'Ортопедія',
    'Хірургія',
]

CATEGORY_START_NAMES = [
    'Консультація оглядова',
    'Одноканальний зуб',
    'Доглядові процедури:',
    'Одноразовий хірургічний набір',
]


def _to_decimal(value: str | None) -> Decimal | None:
    if not value:
        return None
    try:
        return Decimal(value.replace(',', '.').replace(' ', ''))
    except InvalidOperation:
        return None


def _parse_price_value(raw: str) -> dict:
    text = (raw or '').strip()
    lowered = text.lower()
    note = ''
    if 'у.о' in lowered:
        note = 'у.о'
        text = re.sub(r'\s*у\.о\.?', '', text, flags=re.IGNORECASE).strip()

    starts_from = lowered.startswith('від')
    if starts_from:
        text = text[3:].strip()
        lowered = text.lower()

    range_match = re.match(r'^(\d+(?:[.,]\d+)?)\s*-\s*(\d+(?:[.,]\d+)?)$', text)
    if range_match:
        return {
            'price_type': 'range',
            'price': _to_decimal(range_match.group(1)),
            'price_max': _to_decimal(range_match.group(2)),
            'note': note,
        }

    value = _to_decimal(text)
    if value is not None:
        return {
            'price_type': 'from' if starts_from else 'exact',
            'price': value,
            'price_max': None,
            'note': note,
        }

    return {
        'price_type': 'from',
        'price': None,
        'price_max': None,
        'note': note or text,
    }


def _iter_price_pairs(body: str) -> list[tuple[str, str]]:
    lines = [line.strip() for line in body.splitlines()]
    pairs: list[tuple[str, str]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line or line.startswith('#'):
            index += 1
            continue
        if line.startswith('Примітка!') or line.startswith('|'):
            break
        if line.startswith('Затверджено') or line in PRICE_CATEGORY_TITLES:
            index += 1
            continue
        name = line
        price_index = index + 1
        while price_index < len(lines) and not lines[price_index]:
            price_index += 1
        if price_index >= len(lines):
            break
        price = lines[price_index]
        if price and not price.startswith('#') and not price.startswith('|'):
            pairs.append((name, price))
            index = price_index + 1
            continue
        index += 1
    return pairs


def parse_prices() -> dict:
    doc = load_markdown('tsiny.md')
    body = doc.body
    approval_note = ''
    for line in body.splitlines():
        if line.strip().startswith('Затверджено'):
            approval_note = line.strip()
            break

    pairs = _iter_price_pairs(body)
    buckets: dict[str, list[dict]] = {title: [] for title in PRICE_CATEGORY_TITLES}
    current_index = 0

    for name, raw_price in pairs:
        for idx, start_name in enumerate(CATEGORY_START_NAMES):
            if name == start_name:
                current_index = idx
                break
        parsed = _parse_price_value(raw_price)
        buckets[PRICE_CATEGORY_TITLES[current_index]].append({
            'name': name.rstrip(':'),
            **parsed,
        })

    return {
        'title': doc.headings[0]['text'] if doc.headings else 'Ціни',
        'currency_label': 'грн.',
        'approval_note': approval_note,
        'categories': [
            {'title': title, 'items': items}
            for title, items in buckets.items()
            if items
        ],
    }
