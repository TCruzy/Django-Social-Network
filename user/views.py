from rest_framework import viewsets
from user.models import User
from user.serializers import UserListSerializer, UserRetrieveSerializer
from djangoProject.utils.serializers import SerializerFactory


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = SerializerFactory(
        default=UserRetrieveSerializer,
        list=UserListSerializer,
    )
