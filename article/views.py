from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Comment
# Create your views here.


class PostListView(ListView):
    queryset = Post.objects.draft()
    template_name = "article/index.html"


class PostDetailListView(DetailView):
    model = Post
    template_name = "article/post_detail.html"
