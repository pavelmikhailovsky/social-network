from rest_framework import serializers

from . import models


class GroupInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Groups
        fields = [
            'id', 'name', 'image', 'category',
        ]
