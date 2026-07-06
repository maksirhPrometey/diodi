#!/usr/bin/env bash
# Оновлення production Docker-стеку після git pull
set -euo pipefail

APP_DIR="${APP_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$APP_DIR"

COMPOSE_FILE="docker-compose.prod.yml"
if [ ! -d /etc/letsencrypt/live ] || [ -z "$(ls -A /etc/letsencrypt/live 2>/dev/null || true)" ]; then
  echo "==> SSL-сертифікатів немає — HTTP-стек (docker-compose.yml)"
  COMPOSE_FILE="docker-compose.yml"
fi

COMPOSE="docker compose -f ${COMPOSE_FILE}"
HTTP_PORT="${HTTP_PORT:-80}"

if [ ! -f .env ]; then
  echo "FATAL: немає $APP_DIR/.env — скопіюй .env.docker.example"
  exit 1
fi

if ! command -v docker >/dev/null; then
  echo "FATAL: Docker не встановлено. Запусти: bash deploy/docker/install-docker.sh"
  exit 1
fi

# shellcheck disable=SC1091
set -a && source .env && set +a
HTTP_PORT="${HTTP_PORT:-80}"

if [ -z "${POSTGRES_PASSWORD:-}" ]; then
  echo "FATAL: задай POSTGRES_PASSWORD у .env"
  exit 1
fi

if [ -z "${SECRET_KEY:-}" ]; then
  echo "FATAL: задай SECRET_KEY у .env"
  exit 1
fi

free_host_ports() {
  echo "==> Звільняємо порти 80/443 (зупинка nginx/gunicorn на хості)"
  systemctl stop nginx 2>/dev/null || true
  systemctl disable nginx 2>/dev/null || true
  if command -v fuser >/dev/null 2>&1; then
    fuser -k "${HTTP_PORT}/tcp" 2>/dev/null || true
    fuser -k "443/tcp" 2>/dev/null || true
  fi
  sleep 1
  for port in "${HTTP_PORT}" 443; do
    if ss -tlnp 2>/dev/null | grep -q ":${port} "; then
      echo "FATAL: порт ${port} ще зайнятий. Перевір: ss -tlnp | grep :${port}"
      ss -tlnp | grep ":${port} " || true
      exit 1
    fi
  done
}

wait_web_healthy() {
  local i
  for i in $(seq 1 30); do
    if $COMPOSE exec -T web python -c \
      "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz/', timeout=3)" \
      2>/dev/null; then
      return 0
    fi
    sleep 2
  done
  return 1
}

free_host_ports

echo "==> Build images"
$COMPOSE build

echo "==> Up stack"
$COMPOSE up -d

echo "==> Migrations"
$COMPOSE exec -T web python manage.py migrate --noinput

echo "==> Wait for web"
if ! wait_web_healthy; then
  echo "FATAL: web не відповідає на /healthz/"
  $COMPOSE logs --tail=50 web
  exit 1
fi

echo "==> Health via nginx"
if curl -sf "http://127.0.0.1:${HTTP_PORT}/healthz/" >/dev/null; then
  echo "==> HTTP OK"
else
  echo "WARN: HTTP healthz failed (див. docker compose logs nginx)"
fi
if curl -sfk "https://127.0.0.1/healthz/" >/dev/null 2>&1; then
  echo "==> HTTPS OK"
elif [ -d /etc/letsencrypt/live ]; then
  echo "WARN: HTTPS не відповідає — перевір certbot і deploy/nginx/docker.prod.conf"
fi

echo "==> Deploy OK $(date -Iseconds)"
$COMPOSE ps
echo ""
echo "Далі:"
echo "  $COMPOSE exec web python manage.py createsuperuser"
echo "  $COMPOSE exec web python manage.py seed_cms"
