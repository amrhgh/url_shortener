from django.contrib.auth import get_user
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from analytics.models import Analytic
from analytics.serializers import AnalyticListSerializer, AnalyticDetailSerializer


class AnalyticDetailView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AnalyticListSerializer
    detail_serializer_class = AnalyticDetailSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        else:
            return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        return Analytic.objects.filter(url__owner=user)

