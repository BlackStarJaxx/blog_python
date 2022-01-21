from django.contrib import admin
from django.db.models import Count

from .models import Post, Comment, Like


class CommentAdminModelInline(admin.TabularInline):
    model = Comment
    extra = 1


class LikeAdminModelInline(admin.TabularInline):
    model = Like
    extra = 1

    def has_change_permission(self, request, objects):
        return False


# Register your models here.
@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):
    inlines = [
        CommentAdminModelInline,
        LikeAdminModelInline,

    ]
    list_display = ('title', 'slug', 'created', 'user_name', 'count_like')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created',)
    list_filter = ('status', 'created')

    def count_like(self, obj):
        qs = obj.likes.prefetch_related('author').aggregate(likes_count=Count('session_key'))['likes_count']
        return qs

    def user_name(self, obj):
        return obj.author.username

    def qet_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("comments").select_related("author")


@admin.register(Comment)
class CommentAdminModel(admin.ModelAdmin):
    list_display = ('author_comment', 'post', 'created')
    ordering = ('-created',)
    list_filter = ('created',)

# admin.site.register(Post)
# admin.site.register(Comment)
