from api.models import Post, Comment, Group
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer, GroupSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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