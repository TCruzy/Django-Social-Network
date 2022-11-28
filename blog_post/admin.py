from django.contrib import admin
from blog_post.models import Post, PostLikes, Comments, CommentsLikes, Followers
from adminsortable2.admin import SortableAdminMixin
from django.utils.translation import gettext_lazy as _


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'image', 'created_at', 'updated_at')
    list_filter = ('author',)
    search_fields = ('title', 'author__username')


@admin.register(PostLikes)
class PostLikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('user', 'post')
    search_fields = ('user__username', 'post__title')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at')
    list_filter = ('user', 'post')
    search_fields = ('user__username', 'post__title')


@admin.register(CommentsLikes)
class CommentsLikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at')
    list_filter = ('user', 'comment')
    search_fields = ('user__username', 'comment__content')


@admin.register(Followers)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower', 'created_at')
    list_filter = ('user', 'follower')
    search_fields = ('user__username', 'follower__username')


