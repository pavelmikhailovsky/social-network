from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, mixins, parsers, permissions, status, decorators
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from . import serializers, paginations

User = get_user_model()


class UsersViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):
    """ API endpoint for output all users """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    pagination_class = paginations.CustomPageNumberPagination

    def destroy(self, request, *args, **kwargs):
        """ Destroy users if user is staff """
        if self.request.user.is_staff:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        return Response({'permission error': 'user is not staff'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @decorators.action(detail=True, url_path='subscribe-on-user')
    def subscribe_on_user(self, request, *args, **kwargs):
        """ Subscribe on news user """
        if self.request.user.is_authenticated:
            subscribe_user = self.get_object()
            instance = self.request.user
            subscribe_user.subscribers.add(instance)
            instance.subscribed_on_users.add(subscribe_user)
            return Response({'status': 'subscribed'}, status=status.HTTP_200_OK)
        return Response({'status': 'not authorization'}, status=status.HTTP_423_LOCKED)

    def retrieve(self, request, *args, **kwargs):
        """
        If the current user is subscribed to the viewed profile, indicator = 1 otherwise 0
        """
        if self.request.user.is_authenticated:
            instance = self.get_object()
            if self.request.user.subscribed_on_users.get(username=instance.username):
                serializer = serializers.UserWithIndicatorSerializer(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """ API endpoint for create users """
    queryset = User.objects.all()
    serializer_class = serializers.CreateUserSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'status': 'created'}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        # hashing the password for authentication and getting a token in the future
        serializer.validated_data['password'] = make_password(password)
        serializer.save()


class MeUserInformationVewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ API endpoint for output information o user """
    queryset = User.objects.all()
    serializer_class = serializers.MeUserInformationSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={401: '{"detail": "No credentials were provided."}'})
    def list(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(responses={401: '{"detail": "No credentials were provided."}'})
    @decorators.action(detail=False, methods=['patch'], url_path='partial-settings')
    def partial_settings(self, request):
        """ Partial update user account """
        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: '{"status": "deleted"}', 401: '{"detail": "No credentials were provided."}'})
    @decorators.action(detail=False, methods=['delete'], url_path='remove-account')
    def remove_account(self, request):
        """ Remove user account """
        instance = self.request.user
        instance.delete()
        return Response({'status': 'deleted'}, status=status.HTTP_200_OK)
