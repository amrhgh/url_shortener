from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
from urls.models import Url


class Analytic(models.Model):
    url = models.OneToOneField(to=Url, on_delete=models.CASCADE)
    records = JSONField()

    @property
    def url__short_url_path(self):
        return self.url.short_url_path

    def __unicode__(self):
        return self.url.short_url_path