from rest_framework import serializers

from analytics.models import Analytic
from analytics.utils import merge, count_list_items_in_reports


class AnalyticListSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    def get_short_url(self, obj):
        return obj.url.short_url_path

    class Meta:
        model = Analytic
        fields = ['pk', 'short_url']

class AnalyticDetailSerializer(serializers.ModelSerializer):
    url_report = serializers.SerializerMethodField()
    url_unique_report = serializers.SerializerMethodField()

    def get_url_report(self, obj):
        records = dict()
        count_list_items_in_reports(obj.records, records)
        report = dict()
        for value in records.values():
            merge(report, value)
        return report

    def get_url_unique_report(self, obj):
        records = dict()
        count_list_items_in_reports(obj.records, records, unique=True)
        report = dict()
        for value in records.values():
            merge(report, value)
        return report

    class Meta:
        model = Analytic
        fields = ['url_report', 'url_unique_report']
