from rest_framework import serializers
from blog_post.models import Post, PostLikes, Comments, CommentsLikes,Followers
from versatileimagefield.serializers import VersatileImageFieldSerializer


class BasePostSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('square_crop', 'crop__300x300'),
        ]
    )

    class Meta:
        model = Post


class PostListSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        fields = (
            'id',
            'title',
            'content',
            'author',
            'created_at',
        )


class PostRetrieveSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        fields = '__all__'


class PostLikesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikes
        fields = (
            'id',
            'user',
            'post',
            'created_at',
        )


class CommentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = (
            'id',
            'user',
            'post',
            'content',
            'created_at',
        )


class CommentsLikesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsLikes
        fields = (
            'id',
            'user',
            'comment',
            'created_at',
        )


class PostLikesRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikes
        fields = '__all__'


class CommentsRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class CommentsLikesRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsLikes
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = '__all__'