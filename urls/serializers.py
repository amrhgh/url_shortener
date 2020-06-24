import random
import string

from rest_framework import serializers

from url_shortner.settings import SHORT_URL_LENGTH
from urls.models import Url

ALPHA_NUMBERS = string.ascii_letters + string.digits


class UrlSerializer(serializers.ModelSerializer):
    suggested_path = serializers.CharField(max_length=SHORT_URL_LENGTH, write_only=True, required=False)

    def create(self, validated_data):
        pass

    class Meta:
        model = Url
        fields = ['short_url_path', 'long_url', 'suggested_path']
        read_only_fields = ['short_url_path', ]


def generate_random_string(suggested_path=None):
    if suggested_path:
        path = suggested_path
        while True:
            # changing the path string until finds a unique one
            obj = Url.objects.filter(short_url_path=path).first()
            if not obj:
                # if path is not used before
                return path
            index = random.randint(0, SHORT_URL_LENGTH)
            new_char = random.choice(ALPHA_NUMBERS)
            path = path[:index] + new_char + path[index:]  # replace a character with random character

    else:
        # if user doesn't suggest path a random string is generated
        random_string = ''
        for _ in range(SHORT_URL_LENGTH):
            random_string = random_string + random.choice(ALPHA_NUMBERS)
        return random_string
