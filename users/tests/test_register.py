import json

from django.test import TestCase

from rest_framework.test import APIRequestFactory

from users.models import CustomUser
from users.views import RegisterView


class RegisterTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.path = '/register/'
        self.view = RegisterView.as_view()

    def test_register_new_user_not_email_found(self):
        data = json.dumps({'username': 'foo', 'password': 'fooooooo'})
        request = self.factory.post(self.path, data=data,
                                    content_type='application/json')
        response = self.view(request)
        self.assertIn('email', response.data)

    def test_register_new_user_with_correct_data(self):
        data = json.dumps({'email': 'foo@gmail.com', 'username': 'foo', 'password': 'fooooooo'})
        request = self.factory.post(self.path, data=data,
                                    content_type='application/json')
        response = self.view(request)
        self.assertEqual(201, response.status_code)

    def test_register_new_user_with_pre_existing_email(self):
        data = json.dumps({'email': 'new@gmail.com', 'username': 'new', 'password': 'foooooooo'})
        request = self.factory.post(self.path, data=data,
                                    content_type='application/json')
        self.view(request)  # create new user
        request = self.factory.post(self.path, data=data,
                                    content_type='application/json')
        response = self.view(request)
        self.assertIn('email', response.data)
