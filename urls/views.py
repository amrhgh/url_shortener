from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from urls.models import Url
from urls.serializers import UrlSerializer


class UrlView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]

    serializer_class = UrlSerializer

    def get_queryset(self):
        user = self.request.user
        return Url.objects.filter(owner=user)
