from rest_framework import serializers

from analytics.models import Analytic
from analytics.utils import merge, count_list_items_in_reports


class AnalyticSerializer(serializers.ModelSerializer):
    url_report = serializers.SerializerMethodField()

    def get_url_report(self, obj):
        report = dict()
        records = dict()
        count_list_items_in_reports(obj, records)
        for value in records.values():
            merge(report, value)
        return report

    class Meta:
        model = Analytic
        fields= ['url', 'url_report']
