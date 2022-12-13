from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.encoding import force_str
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserListSerializer, UserRetrieveSerializer, SignUpSerializer, TokenCreateSerializer
from djangoProject.utils.serializers import SerializerFactory
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view
from user.utils.token_generators import _OTPVerifyTokenGenerator


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = SerializerFactory(
        default=UserRetrieveSerializer,
        list=UserListSerializer,
    )


class UserCreateView(CreateAPIView):
    serializer_class = UserRetrieveSerializer

    def perform_create(self, serializer):
        serializer.save(is_active=False)

    def create(self, request, **__) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token = _OTPVerifyTokenGenerator.make_token(serializer.instance)
        uid = urlsafe_base64_encode(serializer.instance.pk.to_bytes(4, 'big'))
        return Response({
            'token': token,
            'uid': uid,
            'status': status.HTTP_201_CREATED,
            'headers': headers,
        })


class TokenCreateView(viewsets.GenericViewSet):
    serializer_class = TokenCreateSerializer
    queryset = User.objects.all()

    def create(self, request, **__) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data['user']['email']).first()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response({
            'refresh': str(refresh),
            'access': str(access),
        })


class SignUpView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignUpSerializer


class ActivateUserViewSet(viewsets.GenericViewSet):
    serializer_class = SignUpSerializer

    def get_object(self):
        uid = force_str(urlsafe_base64_decode(self.kwargs['uidb64']))
        user = get_object_or_404(User, id=uid)
        return user

    def activate(self, request, *args, **kwargs):
        user = self.get_object()
        token_generator = _OTPVerifyTokenGenerator()
        if user.is_active:
            return Response({'detail': 'User already activated'}, status=status.HTTP_400_BAD_REQUEST)
        if token_generator.check_token(user, self.kwargs['token']):
            user.is_active = True
            user.save()
            return Response({'detail': 'User activated successfully'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class GetUserDataView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        serializer = UserRetrieveSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    request=None, responses={205: OpenApiTypes.STR},
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data['refresh_token']
    token = RefreshToken(refresh_token)
    token.blacklist()
    return Response(status=status.HTTP_205_RESET_CONTENT)
