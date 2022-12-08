from abc import ABC, abstractmethod

from django.http import Http404
from django.utils.functional import cached_property
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.encoding import force_str, force_bytes, DjangoUnicodeDecodeError
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserListSerializer, UserRetrieveSerializer, OTPSerializer, CustomTokenObtainPairSerializer
from djangoProject.utils.serializers import SerializerFactory
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, OpenApiParameter, extend_schema, inline_serializer

from user.utils.token_generators import OTPVerifyTokenGenerator
from user.utils.permissions import HasValidOTPToken, HasValidRecoverToken


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = SerializerFactory(
        default=UserRetrieveSerializer,
        list=UserListSerializer,
    )


class OTPVerificationViewSet(viewsets.ViewSet, ABC):
    permission_classes = [~IsAuthenticated]
    serializer_class = OTPSerializer

    @abstractmethod
    @cached_property
    def object(self) -> User:
        pass

    @action(methods=['POST'],
            detail=False,
            url_path='send-mail',
            permission_classes=[~IsAuthenticated, HasValidRecoverToken],
            serializer_class=[])
    def send_mail(self, request, *args, **kwargs):

        uid = urlsafe_base64_encode(self.object.pk.to_bytes(4, 'big'))

        token = OTPVerifyTokenGenerator.make_token(self.object)
        # Send the email
        self.object.send_otp_email(uid, token)
        return Response({'detail': 'Email sent successfully.', 'status': 200})


class ActivateUserViewSet(OTPVerificationViewSet):
    permission_classes = [~IsAuthenticated, HasValidOTPToken]
    serializer_class = OTPSerializer

    @cached_property
    def object(self) -> User:
        try:
            user_pk = force_str(urlsafe_base64_decode(self.kwargs['uid']))
        except DjangoUnicodeDecodeError:
            raise Http404
        return get_object_or_404(User, pk=user_pk)

    def create(self, request, **__) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'detail': 'User activated successfully.', 'status': 200})


class UserCreateView(CreateAPIView):
    permission_classes = [~IsAuthenticated]
    serializer_class = UserRetrieveSerializer

    def perform_create(self, serializer):
        serializer.save(is_active=False)

    def create(self, request, **__) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token = OTPVerifyTokenGenerator.make_token(serializer.instance)
        uid = urlsafe_base64_encode(serializer.instance.pk.to_bytes(4, 'big'))
        return Response({
            'token': token,
            'uid': uid,
            'status': status.HTTP_201_CREATED,
            'headers': headers,
        })


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'refresh' in serializer.validated_data:
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.validated_data, status=status.HTTP_302_FOUND)


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
