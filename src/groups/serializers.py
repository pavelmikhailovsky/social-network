from rest_framework import serializers

from . import models


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Groups
        ref_name = 'group'
        fields = ['id', 'name', 'create_at']
