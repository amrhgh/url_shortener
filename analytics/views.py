from django.contrib.auth import get_user
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from analytics.models import Analytic
from analytics.serializers import AnalyticSerializer


class AnalyticDetailView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AnalyticSerializer

    def get_queryset(self):
        user = self.request.user
        return Analytic.objects.filter(url__owner=user)

