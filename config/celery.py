import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery(
    'music_store_exercise',
    backend=settings.CELERY_BACKEND,
    broker=settings.CELERY_BROKER
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
