import redis
from django.conf import settings
from django.contrib.auth import get_user
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import decorator_from_middleware
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from urls.middleware import DataStreamQueue
from urls.models import Url
from urls.serializers import UrlSerializer

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class UrlView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]

    serializer_class = UrlSerializer

    def get_queryset(self):
        user = self.request.user
        return Url.objects.filter(owner=user)


class Redirect(APIView):
    @decorator_from_middleware(DataStreamQueue)
    def get(self, request, path):
        if (url := self.find_long_url(path)) != '':
            return redirect(url)
        else:
            raise NotFound(detail='short url not found')

    def find_long_url(self, path):
        value = redis_instance.get(path)
        if value:  # if key/value cached by redis
            return value.decode()
        url = Url.objects.filter(short_url_path=path).first()
        if url:
            redis_instance.set(path, url.long_url)
            return url.long_url
        redis_instance.set(path, '')
        return ''



