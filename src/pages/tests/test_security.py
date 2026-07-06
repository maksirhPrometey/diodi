"""Тести src/pages/security.py: dev-режим reCAPTCHA і per-IP rate limit."""

import pytest
from django.test import RequestFactory

from src.pages.models import ContactSubmission
from src.pages.security import is_rate_limited, verify_recaptcha


def test_verify_recaptcha_skips_when_secret_not_configured(settings):
    settings.RECAPTCHA_SECRET_KEY = ''
    request = RequestFactory().post('/kontakty/', data={})
    assert verify_recaptcha(request) is True


def test_verify_recaptcha_fails_without_token(settings):
    settings.RECAPTCHA_SECRET_KEY = 'fake-secret-for-test'
    request = RequestFactory().post('/kontakty/', data={})
    assert verify_recaptcha(request) is False


def test_is_rate_limited_false_without_ip():
    assert is_rate_limited(None) is False


@pytest.mark.django_db
def test_is_rate_limited_false_when_no_submissions():
    assert is_rate_limited('127.0.0.1') is False


@pytest.mark.django_db
def test_is_rate_limited_true_after_threshold(settings):
    settings.CONTACT_FORM_RATE_LIMIT_MAX_ATTEMPTS = 2
    for _ in range(2):
        ContactSubmission.objects.create(name='Тест', message='Привіт', ip_address='10.0.0.1')
    assert is_rate_limited('10.0.0.1') is True
