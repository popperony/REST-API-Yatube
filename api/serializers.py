from rest_framework import serializers
from .models import Post, Comment, Group, Follow, User
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title',)
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    following = serializers.SlugRelatedField(read_only=False, queryset=User.objects.all(), slug_field='username')

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow

    def validate(self, value):
        following = get_object_or_404(User, username=value['following'])
        user = self.context['request'].user
        follows = Follow.objects.filter(user=user, following=following)
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(f"Вы уже подписаны на автора {following}") 
        value['following'] = following
        value['user'] = user
        return value
