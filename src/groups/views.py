from rest_framework import viewsets, mixins, parsers, permissions, decorators, status
from rest_framework.response import Response

from . import models, serializers
from ..users import paginations


class GroupInformationViewSet(viewsets.ReadOnlyModelViewSet, mixins.DestroyModelMixin):
    queryset = models.Groups.objects.all()
    serializer_class = serializers.GroupsAllInformationSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    pagination_class = paginations.CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.GroupInformationSerializer
        elif self.action == 'list':
            return self.serializer_class
        elif self.action == 'create_posts':
            return serializers.CreatePostsSerializer
        elif self.action == 'give_all_posts':
            return serializers.PostsGroupSerializer

    @decorators.action(detail=True, url_path='give-all-posts')
    def give_all_posts(self, request, *args, **kwargs):
        """
        Output all posts for current group.
        """
        posts = models.Post.objects.filter(group_id=kwargs['pk']).order_by('-create_at')

        # pagination only for this action
        page = self.paginate_queryset(posts)
        if page:
            serializer = self.get_serializer(posts, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.action(detail=False, methods=['post'], url_path='create-posts')
    def create_posts(self, request, *args, **kwargs):
        """
        Create posts for current group.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'created'}, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=['patch'], url_path='likes-on-posts')
    def likes_on_posts(self, *args, **kwargs):
        """
        Add likes on posts.
        """
        post = models.Post.objects.get(id=kwargs['pk'])
        post.like += 1
        post.save()
        return Response({'count': post.like}, status=status.HTTP_200_OK)

    @decorators.action(detail=True, methods=['delete'], url_path='delete-post')
    def delete_post(self, *args, **kwargs):
        """
        Delete posts.
        """
        post = models.Post.objects.get(id=kwargs['pk'])
        post.delete()
        return Response({'status': 'deleted'}, status=status.HTTP_200_OK)


class CreateGroupViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = models.Groups.objects.all()
    serializer_class = serializers.CreateGroupSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    # permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Create group.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'status': 'created'}, status=status.HTTP_201_CREATED)
















