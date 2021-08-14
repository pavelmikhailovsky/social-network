from rest_framework import viewsets

from . import models, serializers


class GroupViewSet(viewsets.ModelViewSet):
    queryset = models.Groups.objects.all()
    serializer_class = serializers.GroupSerializer
