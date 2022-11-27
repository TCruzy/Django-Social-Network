from rest_framework import viewsets
from blog_post.models import Post, PostLikes, Comments, CommentsLikes, Followers
from blog_post.serializers import PostListSerializer, PostRetrieveSerializer, CommentsRetrieveSerializer \
    , FollowSerializer, PostLikesListSerializer, PostLikesRetrieveSerializer, \
    CommentsListSerializer, CommentsLikesListSerializer, CommentsLikesRetrieveSerializer
from djangoProject.utils.serializers import SerializerFactory

from django.db.models import Count, F, Value
from django.db.models.functions import Length, Upper
from django.db.models.lookups import GreaterThan


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all(
    ).select_related('author').annotate(
        likes_count=Count('post_likes'),
        comments_count=Count('comments'),
    )
    serializer_class = SerializerFactory(
        default=PostRetrieveSerializer,
        list=PostListSerializer,
    )


class PostLikesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PostLikes.objects.all(
    ).select_related('user', 'post').annotate(
        post_title=F('post__title'),
        post_author=F('post__author__first_name'),
    )
    serializer_class = SerializerFactory(
        default=PostLikesRetrieveSerializer,
        list=PostLikesListSerializer,
    )


class CommentsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comments.objects.all(
    ).select_related('user', 'post').annotate(
        post_title=F('post__title'),
        user_username=F('user__first_name'),
    )
    serializer_class = SerializerFactory(
        default=CommentsRetrieveSerializer,
        list=CommentsListSerializer,
    )


class CommentsLikesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommentsLikes.objects.all(
    ).select_related('user', 'comment').annotate(
        comment_content=F('comment__content'),
        comment_post_title=F('comment__post__title'),
        comment_user_username=F('comment__user__first_name'),
        comment_liker_username=F('user__first_name'),
    )
    serializer_class = SerializerFactory(
        default=CommentsLikesRetrieveSerializer,
        list=CommentsLikesListSerializer,
    )


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Followers.objects.all(
    ).select_related('user', 'follower').annotate(
        follower_username=F('follower__first_name'),
        user_username=F('user__first_name'),
    )
    serializer_class = FollowSerializer
