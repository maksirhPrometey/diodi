"""
Docker Compose на Droplet: nginx + gunicorn + PostgreSQL.

DJANGO_SETTINGS_MODULE=config.settings.docker
"""

from .production import *  # noqa: F401, F403

# TLS завершується в nginx; Gunicorn лише HTTP (healthcheck без 301)
SECURE_SSL_REDIRECT = False
