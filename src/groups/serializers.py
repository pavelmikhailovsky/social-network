from rest_framework import serializers

from . import models


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


class GroupInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Groups
        fields = [
            'id', 'name', 'image', 'category',
            'description', 'create_at',
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
            'name', 'image', 'category', 'description',
        ]
