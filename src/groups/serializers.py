from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import serializers

from . import models


User = get_user_model()


class GroupsAllInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Groups
        fields = [
            'id', 'name', 'image', 'category',
        ]


class PostsGroupSerializer(serializers.ModelSerializer):
    text = serializers.ModelField(model_field=models.Post._meta.get_field('text'), required=False)

    class Meta:
        model = models.Post
        fields = [
            'id', 'create_at', 'update_at', 'text',
            'like', 'group', 'image',
        ]


class UserSubscribersGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'image',
        ]


class GroupInformationSerializer(serializers.ModelSerializer):
    owner = UserSubscribersGroupSerializer()
    administrators = UserSubscribersGroupSerializer(many=True)
    subscribers = UserSubscribersGroupSerializer(many=True)
    redactors = UserSubscribersGroupSerializer(many=True)

    class Meta:
        model = models.Groups
        fields = [
            'id', 'name', 'image', 'category',
            'owner', 'administrators', 'redactors',
            'subscribers', 'description', 'create_at',
        ]


class CreatePostsSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=False, required=False)

    class Meta:
        model = models.Post
        fields = [
            'text', 'image', 'group',
        ]


class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Groups
        fields = [
            'id', 'name', 'image', 'category',
            'description',
        ]
