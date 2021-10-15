from django.contrib.auth import get_user_model
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
    like = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = [
            'id', 'create_at', 'update_at', 'text',
            'like', 'image',
        ]

    def get_like(self, obj):
        like = obj.like
        return like.users.all().count()


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

    def create(self, validated_data):
        like = models.Like.objects.create()
        like.save()
        validated_data['like'] = like
        return models.Post.objects.create(**validated_data)


class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Groups
        fields = [
            'id', 'name', 'image', 'category',
            'description',
        ]


class AddPersonalGroupSerializer(serializers.Serializer):
    id_group = serializers.IntegerField()
    id_user = serializers.IntegerField()


class PostIdSerializer(serializers.Serializer):
    id_post = serializers.IntegerField()
