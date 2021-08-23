from rest_framework import viewsets, mixins

from . import models, serializers


class GroupInformationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Groups.objects.all()
    serializer_class = serializers.GroupInformationSerializer
