import os
from datetime import timedelta

import redis
from celery import Celery
from celery.task import periodic_task
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'url_shortner.settings')
app = Celery('analytics')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=1)


@periodic_task(run_every=(timedelta(seconds=10)), ignore_result=False)
def debug_task():
    queue = redis_instance.lrange("data_flow", 0, -1)
    redis_instance.delete("data_flow")
    new_requests_analytics = process_data_from_queue(queue)


def process_data_from_queue(queue):
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
