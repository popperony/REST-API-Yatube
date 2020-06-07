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
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.CharField(source='following.username')
    # following = serializers.SlugRelatedField( #я очень долго бился с этим полем, не победил. TypeError: 'User' object is not subscriptable
    #     many=False
    #     slug_field='username',
    #     queryset=User.objects.all())

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow

    def validate(self, value):
        f = value['following']
        following = get_object_or_404(User, username=f['username'])
        user = self.context['request'].user
        follows = Follow.objects.filter(user=user, following=following)
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(f"Вы уже подписаны на автора {following}") 
        value['following'] = following
        value['user'] = user
        return value
