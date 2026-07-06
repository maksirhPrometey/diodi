"""Налаштування для pytest-django: швидка SQLite in-memory, без реального email/reCAPTCHA."""

from .base import *  # noqa: F401, F403

DEBUG = True
# Фейковий ключ лише для pytest, не production
SECRET_KEY = 'django-insecure-test-only'  # nosec
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# reCAPTCHA вимкнена в тестах (порожньо навмисно, не справжній секрет).
RECAPTCHA_SITE_KEY = ''
RECAPTCHA_SECRET_KEY = ''  # nosec
