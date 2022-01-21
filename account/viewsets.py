from django.contrib.auth import get_user_model
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from article.permission import IsUserOrReadOnly
from article.serializers import PostSerializer
from .serializers import UserSerializer
from core.viewsets import BaseModelViewSet

User = get_user_model()


class UserPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page_size'
    max_page_size = 50


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    pagination_class = UserPagination
    permission_classes = [IsUserOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["first_name", "email", "username", "id"]
    ordering_fields = ["first_name", "username"]
    filterset_fields = ["id", "first_name", "last_name", "email", "username"]

    serializer_class = UserSerializer
    serializer_classes = {
        "posts": PostSerializer
    }

    @action(methods=["GET"], detail=True, url_path="posts")
    def posts(self, request, *args, **kwargs):
        user = self.get_object()
        post_data = user.posts.annotate(like_count=Count('likes'))

        serializer = self.get_serializer(post_data, many=True)

        return Response(serializer.data)
