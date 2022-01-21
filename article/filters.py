import django_filters
from rest_framework import generics
from django_filters import rest_framework as filters

from article.models import Post
from article.serializers import PostSerializer


class PostFilter(django_filters.FilterSet):
    title_1 = filters.CharFilter(field_name="title", lookup_expr='contains')
    slug = filters.CharFilter(field_name="slug", lookup_expr='contains')

    created = django_filters.DateTimeFilter(field_name='created', lookup_expr='day')
    day_created__gt = django_filters.DateTimeFilter(field_name='created', lookup_expr='created__gt')
    day_created__lt = django_filters.DateTimeFilter(field_name='created', lookup_expr='created__lt')

    class Meta:
        model = Post
        fields = ['title', 'slug', 'created']


# class PostList(generics.ListAPIView):
#   #  queryset = Post.objects.all()
#     # serializer_class = PostSerializer
#     filter_backends = filters.DjangoFilterBackend
#     filterset_class = PostFilter


