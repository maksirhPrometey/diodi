import os

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')
workers = int(os.environ.get('WEB_CONCURRENCY', '2'))
worker_class = 'sync'
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
preload_app = True
accesslog = '-'
errorlog = '-'
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info')
