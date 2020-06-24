from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from urls.models import Url
from urls.views import Redirect
from users.models import CustomUser


class RedirectTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.path = reverse('redirect', kwargs={'path': 'shorturl'})
        self.view = Redirect.as_view()

    def test_redirect_path_not_found(self):
        request = self.factory.get(self.path)
        response = self.view(request, 'shorturl')
        self.assertEqual(404, response.status_code)

    def test_redirect_path_found(self):
        user = CustomUser.objects.create(email='foo@gmail.com', username='foo', password='password')
        Url.objects.create(long_url='https://google.com', short_url_path='shorturl', owner=user)
        request = self.factory.get(self.path)
        response = self.view(request, 'shorturl')
        self.assertEqual(302, response.status_code)

