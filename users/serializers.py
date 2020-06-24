from rest_framework import serializers

from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        breakpoint()
        new_user = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        new_user.set_password(self.validated_data['password'])
        new_user.save()
        return new_user

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }
