from django.db import models
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()

POST_STATUS = (
    ("draft", "Draft"),
    ("publish", "Publish")
)


class PostQuerySet(models.QuerySet):
    def draft(self):
        return self.filter(status="draft")

    def publish(self):
        return self.filter(status="publish")


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model)

    def draft(self):
        return self.get_queryset().draft()

    def publish(self):
        return self.get_queryset().publish()


class Post(models.Model):

    def __str__(self):
        return f'{self.id} {self.title}'

    author = models.ForeignKey(User, verbose_name='Name user', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    body = RichTextUploadingField(null=True)
    status = models.CharField(choices=POST_STATUS, max_length=20)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PostManager()

    class Meta:
        default_related_name = "posts"
        ordering = ("created",)


class Comment(models.Model):
    author_comment = models.CharField(verbose_name='Імя Автора: ', max_length=40)
    post = models.ForeignKey(Post, verbose_name='Пости', on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(verbose_name='Поле тексту')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_related_name = "comments"
        ordering = ("created",)


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("post", "session_key"),)
