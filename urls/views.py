from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from urls.models import Url
from urls.serializers import UrlSerializer


class UrlView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]

    serializer_class = UrlSerializer

    def get_queryset(self):
        user = self.request.user
        return Url.objects.filter(owner=user)


class Redirect(APIView):
    def get(self, request, path):
        url = Url.objects.filter(short_url_path=path).first()
        if url:
            return redirect(url.long_url)
        else:
            raise NotFound(detail='short url not found')
