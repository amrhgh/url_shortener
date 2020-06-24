from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        new_user = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        new_user.set_password(self.validated_data['password'])
        new_user.save()
        return new_user

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class CustomJWTSerializer(TokenObtainPairSerializer):
    """
    serializer validator is changed to support login with email
    """
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }
        user_obj = CustomUser.objects.filter(email=attrs.get("username")).first() or CustomUser.objects.filter(
            username=attrs.get("username")).first()
        if user_obj:
            credentials['username'] = user_obj.username
        return super().validate(credentials)
