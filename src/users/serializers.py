from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SubscribeSerializer(serializers.ModelSerializer):
    """
    Serializer for subscriptions.
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'image']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for users.
    """
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    subscribers = SubscribeSerializer(read_only=True, many=True)
    subscribed_on_users = SubscribeSerializer(read_only=True, many=True)

    class Meta:
        model = User
        ref_name = 'user'
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'is_staff', 'is_superuser', 'status', 'image',
            'email', 'subscribers', 'subscribed_on_users',
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        ref_name = 'create'
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'password', 'email', 'status', 'image'
        ]


class MeUserInformationSerializer(UserSerializer):
    """
    Serializer for output information o users.
    """
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(required=False)
    image = serializers.ImageField(read_only=False, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'last_name', 'first_name',
            'password', 'email', 'status', 'image',
            'subscribers', 'subscribed_on_users',
        ]
