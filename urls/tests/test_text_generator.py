from unittest import TestCase

from url_shortner.settings import SHORT_URL_LENGTH
from urls.models import Url
from urls.serializers import generate_random_string
from users.models import CustomUser


class TextGeneratorTest(TestCase):
    def test_generate_text_without_suggest(self):
        text = generate_random_string()
        self.assertEqual(SHORT_URL_LENGTH, len(text))

    def test_generate_text_with_suggest_doesnt_exist_before(self):
        short_url_path = 'shorturl'
        generated_text = generate_random_string(suggested_path=short_url_path)
        self.assertEqual(generated_text, short_url_path)

    def test_generate_text_with_suggest_exists_before(self):
        data = {'email': 'new@gmail.com', 'username': 'new', 'password': 'foooooooo'}
        short_url_path = 'shorturl'
        long_url = 'https://google.com'
        owner = CustomUser.objects.create(**data)
        Url.objects.create(short_url_path=short_url_path, long_url=long_url, owner=owner)
        generated_text = generate_random_string(suggested_path=short_url_path)
        self.assertNotEqual(generated_text, short_url_path)