from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from urls.models import Url
from urls.serializers import UrlSerializer


class UrlView(ModelViewSet):
    permission_classes = [IsAuthenticated, ]

    serializer_class = UrlSerializer

    def get_queryset(self):
        user = self.request.user
        return Url.objects.filter(owner=user)
