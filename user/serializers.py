from rest_framework import serializers
from user.models import User
from versatileimagefield.serializers import VersatileImageFieldSerializer


class BaseUserSerializer(serializers.ModelSerializer):
    profile_picture = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
        ]
    )

    class Meta:
        model = User


class UserListSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
        )


class UserRetrieveSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = '__all__'

