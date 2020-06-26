import os
from datetime import timedelta, datetime

import redis
from django.conf import settings
from celery.task import periodic_task

from analytics.utils import merge

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'url_shortner.settings')

import django
django.setup()

from analytics.models import Analytic
from urls.models import Url
from celery import Celery

app = Celery('analytics')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=1)


@periodic_task(run_every=(timedelta(seconds=3)), ignore_result=False)
def collect_redirect_data():
    """
        this function is run periodically and async by celery beat
        read redirect data queue, clear it and store data in database
    """
    queue = redis_instance.lrange("data_flow", 0, -1)
    redis_instance.delete("data_flow")
    records = process_data_from_queue(queue)
    for key, value in records.items():  # add all records to database one by one
        url = Url.objects.get(short_url_path=key)
        date = str(datetime.today().date())
        analytic = Analytic.objects.filter(url=url).first()
        if not analytic:
            analytic = Analytic.objects.create(url=url, records={})
        if date not in analytic.records:
            analytic.records[date] = dict()
        merge(analytic.records[date], records[key])
        analytic.save()


def process_data_from_queue(queue):
    """
    in storing redirect data in queue, priority was given to speed and data is out of shape
    here data format has changed before storing data in database
    """
    new_requests_analytics = dict()
    for item in queue:
        item = eval(item)
        if not (short_url := item.get('path')) in new_requests_analytics:
            path_dic = dict({'total': list(), 'browser': dict(), 'device': dict()})
            new_requests_analytics[short_url] = path_dic
        else:
            path_dic = new_requests_analytics[short_url]
        browser = path_dic.get('browser')
        device = path_dic.get('device')
        total = path_dic.get('total')
        total.append(item.get('ip'))
        browser.setdefault(item.get('browser'), []).append(item.get('ip'))
        device_type = 'pc' if item.get('is_pc') else 'phone/tablet'
        device.setdefault(device_type, []).append(item.get('ip'))
    return new_requests_analytics




