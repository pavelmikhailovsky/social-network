from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class ImageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = 'image'
        fields = ['avatar_image', 'profile_image']


class UserSerializer(serializers.ModelSerializer):
    image = ImageUserSerializer(read_only=True)

    class Meta:
        model = User
        ref_name = 'user'
        fields = ['id', 'username', 'is_staff', 'is_superuser', 'status', 'image']