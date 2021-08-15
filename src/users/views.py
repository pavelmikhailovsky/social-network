from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins

from . import serializers
from .models import UserImage

User = get_user_model()


class UsersViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CreateUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.CreateUserSerializer


# class ImageUserUpdateViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
#     queryset = UserImage.objects.all()
#     serializer_class = serializers.ImageUserSerializer
#
#     def create(self, request, *args, **kwargs):
#         self.data_request = request.data
#         super(ImageUserUpdateViewSet, self).create(request, *args, **kwargs)
#
#     def add_image_to_user(self):
#         if not self.request.user.is_anonymous:
#             user = User.objects.get(self.request.user)
#             user_image = user.image.add(self.data_request)
#             user_image.save()
#
#     def perform_create(self, serializer):
#         self.add_image_to_user()
#         serializer.save()
#
