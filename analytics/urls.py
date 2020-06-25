from django.urls import path
from rest_framework.routers import DefaultRouter

from analytics.views import AnalyticDetailView

router = DefaultRouter()
router.register('', AnalyticDetailView, basename='analytics')

urlpatterns = router.urls