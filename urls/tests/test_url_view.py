import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from urls.views import UrlView
from users.models import CustomUser


class UrlViewTest(TestCase):
    def setUp(self):
        data = {'email': 'foo@gmail.com', 'username': 'foo', 'password': 'foooooooo'}
        self.user = CustomUser.objects.create(**data)
        self.factory = APIRequestFactory()
        self.path = '/urls/'

    def test_create_new_url(self):
        view = UrlView.as_view()
        data = json.dumps({'long_url': 'https://google.com'})
        request = self.factory.post(self.path, data=data,
                                    content_type='application/json')
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEqual(201, response.status_code)
