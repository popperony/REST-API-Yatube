from api.models import Post, Comment, Group, Follow, User
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group')
        if group is not None:
            queryset = queryset.filter(group_id=group)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all()
        posts_pk = self.kwargs['posts_pk']
        if posts_pk is not None:
            queryset = queryset.filter(post_id=posts_pk)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, posts_pk):
        queryset = self.get_queryset()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=following__username', '=user__username']

    def perform_create(self, serializer):
        following = User.objects.get(username=self.request.data.get('following'))
        user = self.request.user
        follower = Follow.objects.filter(user=user, following=following)
        if follower:
            raise ValidationError('Following field is required.')
        serializer.save(user=user, following=following)
