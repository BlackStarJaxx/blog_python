from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from core.viewsets import BaseModelViewSet
from .filters import PostFilter
from .models import Post, Comment, Like
from .permission import IsOwnerOrReadOnly, IsOwnerCommentOrReadOnly
from .serializers import PostSerializer, CommentSerializer


class PostPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 10


class PostViewSet(BaseModelViewSet):
    queryset = Post.objects.annotate(like_count=Count("likes"), comment_count=Count('comments'))
    filter_class = PostFilter
    pagination_class = PostPagination
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    #  filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]

    # filterset_fields = [ "created", "body", "slug"]
    # ordering_fields = ["title", "created"]
    # search_fields = ["title", "author__first_name", "created", "author__username", "body"]
    ordering = ["created"]

    @action(methods=["POST", "GET"], detail=True, url_path="like", permission_classes=[AllowAny])
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        if self.request.method == "POST":
            session = request.data.get(
                'session_key', self.request.session.session_key or self.request.META["REMOTE_ADDR"]
            )
            if post.likes.filter(session_key=session):
                Like.objects.filter(post=post, session_key=session).delete()
                return Response({"status": "not liked", "likes": post.likes.count()})
            else:
                Like.objects.create(
                    post=post,
                    session_key=session
                )
                return Response({"status": "liked", "likes": post.likes.count()})
        return Response(post.likes.count())

    @action(methods=["GET"], detail=False, url_path="top")
    def top(self, request, *args, **kwargs):
        top = int(request.query_params.get('top', 10))
        like = self.get_queryset().order_by("-like_count")[:top]
        serializer = self.get_serializer(like, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, url_path="get_top_comments", permission_classes=[AllowAny])
    def get_top_comments(self, request, *args, **kwargs):
        top = int(request.query_params.get('top', 10))
        comment = self.queryset.annotate().order_by("-comment_count")[:top]
        serializer = self.get_serializer(comment, many=True)
        return Response(serializer.data)


class CommentViewSet(NestedViewSetMixin, BaseModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerCommentOrReadOnly]

    def get_serializer(self, *args, **kwargs):
        if kwargs.get("data"):
            kwargs["data"].update(self.get_parents_query_dict())
        return super(CommentViewSet, self).get_serializer(*args, **kwargs)
