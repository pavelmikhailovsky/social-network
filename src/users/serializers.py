from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import UserImage

User = get_user_model()


class ImageUserSerializer(FlexFieldsModelSerializer):
    avatar = VersatileImageFieldSerializer(required=False, sizes=[('full_size', 'url')])

    class Meta:
        model = UserImage
        fields = ('avatar',)


class UserSerializer(FlexFieldsModelSerializer):
    image = ImageUserSerializer()

    class Meta:
        model = User
        ref_name = 'user'
        fields = ('id', 'username', 'is_staff', 'is_superuser', 'status', 'image')


class CreateUserSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        ref_name = 'create'
        fields = ['username', 'password', 'email', 'status']
