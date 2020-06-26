import random
import string

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from url_shortner.settings import SHORT_URL_LENGTH
from urls.models import Url

ALPHA_NUMBERS = string.ascii_lowercase + string.digits


class UrlSerializer(serializers.ModelSerializer):
    suggested_path = serializers.CharField(max_length=SHORT_URL_LENGTH, write_only=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_suggested_path(self, value):
        value = value.lower()
        if len(value) != 8:
            raise ValidationError({'suggested_path': "Ensure this field has no less than 8 characters."})
        if not set(value).issubset(ALPHA_NUMBERS):
            raise ValidationError({'suggested_path': "invalid input, only [a-zA-Z0-9] are permitted"})
        return value

    def save(self):
        short_url_path = generate_random_string(self.validated_data.get('suggested_path'))
        obj = Url.objects.create(short_url_path=short_url_path, long_url=self.validated_data.get('long_url'),
                                 owner=self.validated_data.get('user'))
        return obj


    class Meta:
        model = Url
        fields = ['id', 'short_url_path', 'long_url', 'suggested_path', 'user']
        read_only_fields = ['id', 'short_url_path', ]


def generate_random_string(suggested_path=None, length=SHORT_URL_LENGTH):
    if suggested_path:
        path = suggested_path
        while True:
            # changing the path string until finds a unique one
            obj = Url.objects.filter(short_url_path=path).first()
            if not obj:
                # if path is not used before
                return path
            index = random.randint(0, length - 1)
            new_char = random.choice(ALPHA_NUMBERS)
            path = path[:index] + new_char + path[index + 1:]  # replace a character with random character

    else:
        # if user doesn't suggest path a random string is generated
        random_string = ''
        for _ in range(length):
            random_string = random_string + random.choice(ALPHA_NUMBERS)
        return random_string
