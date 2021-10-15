from rest_framework import viewsets, mixins, parsers, permissions, decorators, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from . import models, serializers
from .services import CheckingRoleUserCurrentGroup, GetObjectsQuerySet
from ..users import paginations


class GroupInformationViewSet(viewsets.ReadOnlyModelViewSet, mixins.DestroyModelMixin):
    queryset = models.Groups.objects.all()
    serializer_class = serializers.GroupsAllInformationSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        elif self.action == 'retrieve':
            return serializers.GroupInformationSerializer
        elif self.action == 'create_posts':
            return serializers.CreatePostsSerializer
        elif self.action == 'give_all_posts':
            return serializers.PostsGroupSerializer
        elif self.action == 'add_administrators':
            return serializers.AddPersonalGroupSerializer
        elif self.action == 'delete_post' or 'likes_on_posts' or 'like_checking':
            return serializers.PostIdSerializer

    @decorators.action(detail=True, url_path='give-all-posts')
    def give_all_posts(self, *args, **kwargs):
        """
        Output all posts for current group.
        """
        posts = models.Post.objects.filter(group_id=kwargs['pk']).order_by('-create_at')
        self.pagination_class = paginations.CustomPageNumberPagination

        # pagination only for this action
        page = self.paginate_queryset(posts)
        if page:
            serializer = self.get_serializer(posts, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @swagger_auto_schema(method='patch', responses={201: '{"": "created"}'})
    @decorators.action(detail=False, methods=['post'], url_path='create-posts')
    def create_posts(self, *args, **kwargs):
        """
        Create posts for current group.
        """
        user = CheckingRoleUserCurrentGroup(self.request.data['group'], self.request.user.id)

        if user.is_owner() or user.is_administrator() or user.is_redactor():
            serializer = self.get_serializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 'created'}, status=status.HTTP_201_CREATED)

        return Response(
            {'permission error': 'user not permission for this action'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @decorators.action(detail=False, methods=['patch'], url_path='likes-on-posts')
    def likes_on_posts(self, *args, **kwargs):
        """
        Add likes on posts.
        """
        post = models.Post.objects.get(id=self.request.data['id_post'])
        like = post.like

        if self.request.user.is_authenticated:

            if not like.users.filter(id=self.request.user.id):
                like.users.add(self.request.user)
                return Response({'status': 'liked'}, status=status.HTTP_200_OK)

            like.users.remove(self.request.user)
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)

        return Response({'authorization': 'user not authorization'}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        method='patch',
        responses={200: '{"status": "deleted"}',
                   405: '{"permission error": "action not allowed"}',
                   401: '{"authentication": "user is not authentication"}'}
    )
    @decorators.action(detail=True, methods=['patch'], url_path='delete-post')
    def delete_post(self, *args, **kwargs):
        """
        Delete posts.
        """
        if self.request.user.is_authenticated:
            user = CheckingRoleUserCurrentGroup(kwargs['pk'], self.request.user.id)

            if user.is_owner() or user.is_administrator() or self.request.user.is_staff:
                post = models.Post.objects.get(id=self.request.data['id_post'])
                post.delete()
                return Response({'status': 'deleted'}, status=status.HTTP_200_OK)

            return Response({'permission error': 'action not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return Response({'authentication': 'user is not authentication'}, status=status.HTTP_401_UNAUTHORIZED)

    @decorators.action(detail=False, methods=['patch'], url_path='add-administrators')
    def add_administrators(self, *args, **kwargs):
        """
        Add new administrators in group.
        """
        # current user
        user = CheckingRoleUserCurrentGroup(self.request.data['id_group'], self.request.user.id)

        # user who will awarded the title of administrator
        add_user = CheckingRoleUserCurrentGroup(self.request.data['id_group'], self.request.data['id_user'])

        if user.is_owner() or user.is_administrator():
            # getting objects user and group for addition "add_user" in admin team
            obj = GetObjectsQuerySet(self.request.data['id_user'], self.request.data['id_group'])

            if add_user.is_subscriber() and not add_user.is_administrator():

                if add_user.is_redactor():
                    obj.group.redactors.remove(obj.user)

                obj.group.administrators.add(obj.user)
                obj.group.save()
                return Response(
                    {'status': f'user {obj.user.username} added in administrators group'},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {'status': f'user {obj.user.username} is not a subscriber or he is an administrator'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return Response(
            {'status': 'user is not owner or administrator'}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @decorators.action(detail=False, methods=['patch'], url_path='add-redactors')
    def add_redactors(self, *args, **kwargs):
        """
        Add new redactors in group.
        """
        # current user
        user = CheckingRoleUserCurrentGroup(self.request.data['id_group'], self.request.user.id)

        # user who will awarded the title of redactor
        add_user = CheckingRoleUserCurrentGroup(self.request.data['id_group'], self.request.data['id_user'])

        if user.is_owner() or user.is_administrator():
            # getting objects user and group for addition "add_user" in redactor team
            obj = GetObjectsQuerySet(self.request.data['id_user'], self.request.data['id_group'])

            if add_user.is_subscriber() and not add_user.is_redactor():

                if add_user.is_administrator():
                    obj.group.administrators.remove(obj.user)

                obj.group.redactors.add(obj.user)
                obj.group.save()
                return Response(
                    {'status': f'user {obj.user.username} added in redactors group'},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {'status': f'user {obj.user.username} is not a subscriber or he is an redactor'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return Response(
            {'status': 'user is not owner or administrator'}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @decorators.action(detail=True, methods=['patch'], url_path='follow-on-group')
    def follow_on_group(self, *args, **kwargs):
        """
        Follow/unfollow current user on groups.
        """
        if self.request.user.is_authenticated:
            current_group = self.get_object()
            user = CheckingRoleUserCurrentGroup(current_group.id, self.request.user.id)

            if not user.is_subscriber():
                current_group.subscribers.add(self.request.user)
                return Response({'status': 'subscribed'}, status=status.HTTP_200_OK)
            else:
                current_group.subscribers.remove(self.request.user)

                if user.is_administrator():
                    current_group.administrators.remove(self.request.user)
                elif user.is_redactor():
                    current_group.redactors.remove(self.request.user)

                return Response({'status': 'unsubscribed'}, status=status.HTTP_200_OK)

        return Response(
            {'authorization error': 'user is not authorization'}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @decorators.action(detail=False, url_path='like-checking')
    def like_checking(self, *args, **kwargs):
        """
        Checking like/unlike on current post, "true" if user like on post, otherwise "false".
        """
        if self.request.user.is_authenticated:
            post = models.Post.objects.get(id=self.request.data['id_post'])
            like = post.like

            try:
                like.users.get(id=self.request.user.id)
                return Response({'like': True}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'like': False}, status=status.HTTP_200_OK)

        return Response(
            {'authorization info': 'user is not authorization'}, status=status.HTTP_401_UNAUTHORIZED
        )

    @decorators.action(detail=True, url_path='checking-follow')
    def checking_follow(self, *args, **kwargs):
        """
        Checking follow/unfollow on current group, "true" if user follow on group, otherwise "false".
        """
        if self.request.user.is_authenticated:
            user = CheckingRoleUserCurrentGroup(kwargs['pk'], self.request.user.id)

            if user.is_subscriber():
                return Response({'follow': True}, status=status.HTTP_200_OK)

            return Response({'follow': False}, status=status.HTTP_200_OK)

        return Response(
            {'authorization info': 'user is not authorization'}, status=status.HTTP_401_UNAUTHORIZED
        )


class CreateGroupViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = models.Groups.objects.all()
    serializer_class = serializers.CreateGroupSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, *args, **kwargs):
        """
        Create group.
        """
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        group = models.Groups.objects.get(id=serializer.data['id'])
        group.subscribers.add(self.request.user)
        return Response({'status': 'created'}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
