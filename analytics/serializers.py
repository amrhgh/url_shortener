from rest_framework import serializers

from analytics.models import Analytic
from analytics.utils import merge, count_list_items_in_reports


class AnalyticSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    def get_short_url(self, obj):
        return obj.url.short_url_path

    class Meta:
        model = Analytic
        fields = ['pk', 'short_url']
