from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        ref_name = 'user'
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'status', 'image', 'email')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = 'create'
        fields = ['first_name', 'last_name', 'password', 'email', 'status', 'image']
