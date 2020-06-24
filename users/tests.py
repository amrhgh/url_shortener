import json

from django.test import TestCase

from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import CustomUser
from users.views import RegisterView, CustomTokenObtainPairView





class ObtainJWTToken(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.path = '/token/'
        self.view = CustomTokenObtainPairView.as_view()
        self.create_new_user()

    def create_new_user(self):
        data = {'email': 'user@gmail.com', 'username': 'user', 'password': 'useruser'}
        new_user = CustomUser(
            email=data['email'],
            username=data['username'],
        )
        new_user.set_password(data['password'])
        new_user.save()
        return new_user

    def test_obtain_token_with_email(self):
        data = json.dumps({'username': 'user@gmail.com', 'password': 'useruser'})
        request = self.factory.post(self.path, data=data,
                                    content_type='application/json')
        response = self.view(request)
        self.assertEqual(200, response.status_code)

    def test_obtain_token_username_not_found(self):
        data = json.dumps({'password': 'useruser'})
        request = self.factory.post(self.path, data=data,
                                    content_type='application/json')
        response = self.view(request)
        self.assertIn('username', response.data)
