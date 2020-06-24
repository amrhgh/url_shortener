import json

from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory

from users.views import RegisterView


class RegisterTest(TestCase):
    def test_register_new_user_not_email_found(self):
        factory = APIRequestFactory()
        request = factory.post('/register/', json.dumps({'username': 'foo', 'password': 'fooooooo'}),
                               content_type='application/json')
        view = RegisterView.as_view()

        response = view(request)
        self.assertIn('email', response.data)