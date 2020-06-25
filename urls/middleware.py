import json
from datetime import datetime

import redis
from django.conf import settings
from user_agents import parse

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=1)


class DataStreamQueue:
    def process_response(self, request, response):
        user_agent = parse(request.request.META['HTTP_USER_AGENT'])
        user_address = request.request.META['REMOTE_ADDR']
        path = request.kwargs.get('path')
        redis_instance.lpush('data_flow', str({'browser': user_agent.browser.family,
                                               'is_pc': user_agent.is_pc,
                                               'ip': user_address,
                                               'path': path}))
        return response
