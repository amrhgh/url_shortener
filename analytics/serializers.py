from datetime import datetime, timedelta

from rest_framework import serializers

from analytics.models import Analytic
from analytics.utils import merge, count_list_items_in_reports

intervals = {
    'today': (datetime.today().date(), datetime.today().date()),
    'yesterday': (datetime.today().date() - timedelta(days=1), datetime.today().date() - timedelta(days=1)),
    "last_week": (datetime.today().date() - timedelta(days=7), datetime.today().date() - timedelta(days=1)),
    "last_month": (datetime.today().date() - timedelta(days=30), datetime.today().date() - timedelta(days=1))
}


# query = self.context['request'].query_params.get('q', None)

class AnalyticListSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    def get_short_url(self, obj):
        return obj.url.short_url_path

    class Meta:
        model = Analytic
        fields = ['pk', 'short_url']


class AnalyticDetailSerializer(serializers.ModelSerializer):
    url_report = serializers.SerializerMethodField()

    def get_url_report(self, obj):
        valid_records = self.filter_records_by_time(obj)
        records = dict()
        unique_records = dict()
        count_list_items_in_reports(valid_records, records, unique_records)
        not_unique_ip_report = dict()
        unique_ip_report = dict()
        for value in records.values():
            merge(not_unique_ip_report, value)
        for value in unique_records.values():
            merge(unique_ip_report, value)
        return {'not_unique_ip': not_unique_ip_report, 'unique_ip': unique_ip_report}

    def filter_records_by_time(self, obj):
        intervals = {
            'today': (datetime.today().date(), datetime.today().date()),
            'yesterday': (datetime.today().date() - timedelta(days=1), datetime.today().date() - timedelta(days=1)),
            "last_week": (datetime.today().date() - timedelta(days=7), datetime.today().date() - timedelta(days=1)),
            "last_month": (datetime.today().date() - timedelta(days=30), datetime.today().date() - timedelta(days=1))
        }
        query = self.context['request'].query_params.get('q', 'today')
        interval = intervals.get(query)

        valid_keys = [key for key in obj.records.keys() if
                      interval[0] <= datetime.strptime(key, '%Y-%m-%d').date() <= interval[1]]
        return {k: v for k, v in obj.records.items() if k in valid_keys}

    class Meta:
        model = Analytic
        fields = ['url_report']
