# Create your views here.
from rest_framework import generics
from rest_framework_simplejwt.views import TokenViewBase

from users.serializers import RegisterSerializer, CustomJWTSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenViewBase):
    """
    change default token obtain pair view to support email/username login
    """
    serializer_class = CustomJWTSerializer