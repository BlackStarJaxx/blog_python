from rest_framework import serializers

from account.serializers import UserSerializer
from .models import Post, Comment
from django.contrib.auth import get_user_model

from core.serializers import BaseModelSerializer

User = get_user_model()


class CommentSerializer(BaseModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source="post"
    )

    class Meta:
        model = Comment
        fields = ('id', 'author_comment', 'body', "post_id")


class PostSerializer(BaseModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="author"
    )

    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('id', 'slug', 'title', 'body', 'created', 'comments',
                  'author_id', 'like_count', 'comment_count')
