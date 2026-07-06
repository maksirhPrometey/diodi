#!/usr/bin/env bash
set -euo pipefail

cd /app

echo "==> Waiting for PostgreSQL..."
python <<'PY'
import os
import sys
import time

import psycopg2

host = os.environ.get('DB_HOST', 'db')
port = os.environ.get('DB_PORT', '5432')
name = os.environ.get('POSTGRES_DB', 'diodi')
user = os.environ.get('POSTGRES_USER', 'diodi')
password = os.environ.get('POSTGRES_PASSWORD', '')

if not password:
    sys.exit(0)

for attempt in range(30):
    try:
        psycopg2.connect(
            dbname=name,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        print('==> DB ready')
        break
    except psycopg2.OperationalError:
        time.sleep(2)
else:
    print('FATAL: DB not ready')
    sys.exit(1)
PY

echo "==> Django check"
python manage.py check

echo "==> Migrations"
python manage.py migrate --noinput

echo "==> Collectstatic"
python manage.py collectstatic --noinput

mkdir -p staticfiles media
touch staticfiles/.keep media/.keep

echo "==> Start: $*"
exec "$@"
