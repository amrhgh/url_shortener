from django.db import models

# Create your models here.
from users.models import CustomUser

SHORT_URL_LENGTH = 64


class Url(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    long_url = models.URLField()
    short_url_path = models.CharField(max_length=SHORT_URL_LENGTH, unique=True)

    def __str__(self):
        return f'{self.owner} -- {self.short_url_path}'