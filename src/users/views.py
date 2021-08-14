from django.contrib.auth import get_user_model
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema

from . import serializers


User = get_user_model()


class GetAllUsers(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
