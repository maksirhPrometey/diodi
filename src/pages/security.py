"""Захист форм заявок: reCAPTCHA v2 (server-side verify) і per-IP rate limit."""

from __future__ import annotations

import json
import logging
from datetime import timedelta
from urllib import parse as urlparse
from urllib import request as urlrequest
from urllib.error import URLError

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

RECAPTCHA_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'


def verify_recaptcha(request) -> bool:
    """True, якщо reCAPTCHA не налаштована (dev) або токен підтверджено Google.

    Порожній RECAPTCHA_SECRET_KEY означає, що деплой ще не сконфігуровано —
    у цьому разі перевірка пропускається, щоб не блокувати локальну розробку.
    """
    secret = settings.RECAPTCHA_SECRET_KEY
    if not secret:
        return True

    token = request.POST.get('g-recaptcha-response', '')
    if not token:
        return False

    payload = urlparse.urlencode({
        'secret': secret,
        'response': token,
        'remoteip': request.META.get('REMOTE_ADDR', ''),
    }).encode()

    try:
        # URL захардкоджена константа (офіційний Google endpoint), не user input
        with urlrequest.urlopen(RECAPTCHA_VERIFY_URL, data=payload, timeout=5) as response:  # nosec
            result = json.loads(response.read().decode())
    except (URLError, TimeoutError, ValueError) as exc:
        logger.error('Помилка перевірки reCAPTCHA: %s', exc)
        return False

    return bool(result.get('success'))


def is_rate_limited(ip_address: str | None) -> bool:
    """True, якщо з цієї IP надіслано забагато заявок за останнє вікно часу."""
    if not ip_address:
        return False

    from src.pages.models import ContactSubmission

    window_start = timezone.now() - timedelta(seconds=settings.CONTACT_FORM_RATE_LIMIT_WINDOW_SECONDS)
    recent_count = ContactSubmission.objects.filter(
        ip_address=ip_address,
        created_at__gte=window_start,
    ).count()
    return recent_count >= settings.CONTACT_FORM_RATE_LIMIT_MAX_ATTEMPTS
