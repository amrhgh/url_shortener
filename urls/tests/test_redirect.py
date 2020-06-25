from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient

from urls.middleware import redis_instance
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
        response = self.view(request, 'shortirl')
        self.assertEqual(404, response.status_code)

    def test_redirect_path_found(self):
        user = CustomUser.objects.create(email='foo@gmail.com', username='foo', password='password')
        Url.objects.create(long_url='https://google.com', short_url_path='shorturl', owner=user)
        HTTP_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        request = self.factory.get(self.path, HTTP_USER_AGENT=HTTP_USER_AGENT,
                   REMOTE_ADDR='localhost')
        response = self.view(request, 'shorturl')
        self.assertEqual(302, response.status_code)

    def test_redis_track_data_flow(self):
        user = CustomUser.objects.create(email='foo@gmail.com', username='foo', password='password')
        Url.objects.create(long_url='https://google.com', short_url_path='shorturl', owner=user)
        lst = redis_instance.lrange('data_flow', 0, -1)
        client = APIClient()
        HTTP_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        client.get('/r/shorturl',
                   HTTP_USER_AGENT=HTTP_USER_AGENT,
                   REMOTE_ADDR='localhost')
        new_lst = redis_instance.lrange('data_flow', 0, -1)
        self.assertEqual(len(lst) + 1, len(new_lst))
