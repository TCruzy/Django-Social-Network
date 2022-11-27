from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from djangoProject.utils.custom_fields import CustomVersatileImageField


class Post(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=255)
    content = RichTextUploadingField(verbose_name=_('content'))
    image = CustomVersatileImageField(
        verbose_name=_('image'),
        upload_to='blog_post_images',
    )
    author = models.ForeignKey(
        'user.User',
        verbose_name=_('author'),
        on_delete=models.CASCADE,
        related_name='posts',
    )
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class PostLikes(models.Model):
    user = models.ForeignKey(
        'user.User',
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='post_likes_user',
    )
    post = models.ForeignKey(
        'blog_post.Post',
        verbose_name=_('post'),
        on_delete=models.CASCADE,
        related_name='post_likes',
    )
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('post like')
        verbose_name_plural = _('post likes')
        ordering = ('-created_at',)
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} liked {self.post}'


class Followers(models.Model):
    user = models.ForeignKey(
        'user.User',
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='followers',
    )
    follower = models.ForeignKey(
        'user.User',
        verbose_name=_('follower'),
        on_delete=models.CASCADE,
        related_name='following',
    )
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('follower')
        verbose_name_plural = _('followers')
        ordering = ('-created_at',)
        unique_together = ('user', 'follower')

    def __str__(self):
        return f'{self.follower} follows {self.user}'


class Comments(models.Model):
    user = models.ForeignKey(
        'user.User',
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='comments',
    )
    post = models.ForeignKey(
        'blog_post.Post',
        verbose_name=_('post'),
        on_delete=models.CASCADE,
        related_name='comments',
    )
    content = models.TextField(verbose_name=_('content'))
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user} commented on {self.post}'


class CommentsLikes(models.Model):
    user = models.ForeignKey(
        'user.User',
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='comment_likes',
    )
    comment = models.ForeignKey(
        'blog_post.Comments',
        verbose_name=_('comment'),
        on_delete=models.CASCADE,
        related_name='comment_likes',
    )
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('comment like')
        verbose_name_plural = _('comment likes')
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user} liked {self.comment}'
