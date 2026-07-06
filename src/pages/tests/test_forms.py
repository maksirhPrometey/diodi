"""Тести ContactForm і повного flow подачі заявки через HTMX partial-view."""

import pytest

from src.pages.forms import ContactForm
from src.pages.models import ContactSubmission


def test_callback_form_valid():
    form = ContactForm(
        data={'name': 'Олена', 'phone': '+380501234567', 'message': 'Питання'},
        form_type=ContactSubmission.FORM_CALLBACK,
    )
    assert form.is_valid(), form.errors


def test_callback_form_rejects_short_phone():
    form = ContactForm(
        data={'name': 'Олена', 'phone': '123', 'message': 'Питання'},
        form_type=ContactSubmission.FORM_CALLBACK,
    )
    assert not form.is_valid()
    assert 'phone' in form.errors


def test_email_form_requires_email():
    form = ContactForm(
        data={'name': 'Олена', 'message': 'Питання'},
        form_type=ContactSubmission.FORM_EMAIL,
    )
    assert not form.is_valid()
    assert 'email' in form.errors


@pytest.mark.django_db
def test_contact_form_partial_view_saves_submission(client):
    response = client.post(
        '/forms/callback/',
        data={'form_type': 'callback', 'name': 'Олена', 'phone': '0501234567', 'message': 'Питання'},
        HTTP_HX_REQUEST='true',
    )
    assert response.status_code == 200
    assert ContactSubmission.objects.count() == 1


@pytest.mark.django_db
def test_contact_form_partial_view_rate_limited(client, settings):
    settings.CONTACT_FORM_RATE_LIMIT_MAX_ATTEMPTS = 1
    payload = {'form_type': 'callback', 'name': 'Олена', 'phone': '0501234567', 'message': 'Питання'}
    client.post('/forms/callback/', data=payload, HTTP_HX_REQUEST='true')
    response = client.post('/forms/callback/', data=payload, HTTP_HX_REQUEST='true')
    assert response.status_code == 429
