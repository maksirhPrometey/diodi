"""Копіювання зображень з content/legacy/images у Django ImageField."""

from __future__ import annotations

from pathlib import Path

from django.core.files import File

LEGACY_ROOT = Path(__file__).resolve().parent.parent.parent / 'content' / 'legacy'
IMAGES_DIR = LEGACY_ROOT / 'images'


def legacy_image_path(rel_path: str) -> Path | None:
    if not rel_path:
        return None
    cleaned = rel_path.removeprefix('../images/').lstrip('/')
    candidate = IMAGES_DIR / cleaned
    if candidate.exists():
        return candidate
    name = Path(cleaned).name
    for match in IMAGES_DIR.rglob(name):
        return match
    return None


def image_rel_from_markdown(markdown_path: str) -> str:
    return markdown_path.removeprefix('../images/').lstrip('/')


def image_rel_from_url(url: str) -> str | None:
    if not url:
        return None
    marker = '/images/'
    if marker not in url:
        return None
    return url.split(marker, 1)[1]


def attach_image(instance, field_name: str, rel_path: str | None, *, skip_images: bool = False) -> bool:
    if skip_images or not rel_path:
        return False
    source = legacy_image_path(rel_path)
    if source is None:
        return False
    field = getattr(instance, field_name)
    with source.open('rb') as handle:
        field.save(source.name, File(handle), save=False)
    return True
