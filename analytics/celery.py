import os
from datetime import timedelta

from celery import Celery
from celery.task import periodic_task
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'url_shortner.settings')
app = Celery('analytics')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@periodic_task(run_every=(timedelta(seconds=5)), ignore_result=False)
def debug_task():
    print('Request: {0!r}')