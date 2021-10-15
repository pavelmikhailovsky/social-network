from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, mixins, parsers, permissions, status, decorators
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from . import serializers, paginations
from .permissions import IsNotAuthenticated

User = get_user_model()


class UsersViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):
    """
    API endpoint for output all users.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    pagination_class = paginations.CustomPageNumberPagination

    @swagger_auto_schema(responses={200: '{"status": "deleted"}', 405: '{"permission error": "user is not staff"}'})
    def destroy(self, request, *args, **kwargs):
        """
        Destroy users if user is staff.
        """
        if self.request.user.is_staff:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'status': 'deleted'}, status=status.HTTP_200_OK)
        return Response({'permission error': 'user is not staff'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(responses=
                         {200: '{"status": "subscribed or unsubscribed"}', 423: '{"status": "not authorization"}'})
    @decorators.action(detail=True, url_path='follow')
    def follow(self, *args, **kwargs):
        """
        Follow/unfollow on news user.
        """
        if self.request.user.is_authenticated:
            subscribe_user = self.get_object()
            current_user = self.request.user

            if not subscribe_user.subscribers.filter(id=current_user.id):
                subscribe_user.subscribers.add(current_user)
                current_user.subscribed_on_users.add(subscribe_user)
                return Response({'status': 'subscribed'}, status=status.HTTP_200_OK)
            else:
                subscribe_user.subscribers.remove(current_user)
                current_user.subscribed_on_users.remove(subscribe_user)
                return Response({'status': 'unsubscribed'}, status=status.HTTP_200_OK)

        return Response({'status': 'not authorization'}, status=status.HTTP_423_LOCKED)

    @swagger_auto_schema(responses={200: '{"follow": "true of false"}', 423: '{"follow": "not authorization"}'})
    @decorators.action(detail=True, url_path='check-follow')
    def check_follow(self, *args, **kwargs):
        """
        If the current user is subscribed to the viewed profile, follow = true otherwise false.
        """
        if self.request.user.is_authenticated:
            instance = self.get_object()

            try:
                if self.request.user.subscribed_on_users.get(username=instance.username):
                    return Response({'follow': True}, status=status.HTTP_200_OK)
            except Exception as e:
                print(f'>>>> {e}')
                return Response({'follow': False}, status=status.HTTP_200_OK)

        return Response({'status': 'not authorization'}, status=status.HTTP_423_LOCKED)


class CreateUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    API endpoint for create users.
    """
    queryset = User.objects.all()
    serializer_class = serializers.CreateUserSerializer
    permission_classes = [IsNotAuthenticated]
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
    """
    API endpoint for output information o user.
    """
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
        """
        Partial update user account.
        """
        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: '{"status": "deleted"}', 401: '{"detail": "No credentials were provided."}'})
    @decorators.action(detail=False, methods=['delete'], url_path='remove-account')
    def remove_account(self, request):
        """
        Remove user account.
        """
        instance = self.request.user
        instance.delete()
        return Response({'status': 'deleted'}, status=status.HTTP_200_OK)
