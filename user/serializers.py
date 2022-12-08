from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from versatileimagefield.serializers import VersatileImageFieldSerializer
from user.utils.token_generators import OTPVerifyTokenGenerator

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


class OTPSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    hash_key = serializers.CharField(required=True, max_length=255)

    def validate(self, attrs):
        code = attrs.get('code')
        hash_key = attrs.get('hash_key')
        user = User.objects.filter(otp_hash_key=hash_key).first()
        if not user:
            raise AuthenticationFailed({'message': 'Invalid OTP'})
        if not OTPVerifyTokenGenerator().check_token(user, code):
            raise AuthenticationFailed({'message': 'Invalid OTP'})
        return {
            'user': user,
        }


class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        data = {}
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user.is_active:
                    refresh = self.get_token(user)
                    data['refresh'] = str(refresh)
                    data['access'] = str(refresh.access_token)
                    if api_settings.UPDATE_LAST_LOGIN:
                        update_last_login(None, user)
                else:
                    data['token'] = OTPVerifyTokenGenerator().make_token(user)
                    data['uid'] = urlsafe_base64_encode(str(user.pk).encode())
            else:
                raise AuthenticationFailed({'password': 'Wrong password'})
        except User.DoesNotExist:
            raise AuthenticationFailed({'email': 'User does not exist'})

        return data