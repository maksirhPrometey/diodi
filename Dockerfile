FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=config.settings.docker

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

RUN mkdir -p staticfiles media \
    && chmod +x deploy/docker/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/deploy/docker/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "-c", "deploy/gunicorn_docker.conf.py"]
