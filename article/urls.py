from django.urls import path

from .views import PostListView, PostDetailListView

urlpatterns = [
    path('', PostListView.as_view(), name='main'),
    path('<slug:slug>/', PostDetailListView.as_view(), name='post_detail'),
]
