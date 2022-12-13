from django.contrib.auth.models import update_last_login
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken

from djangoProject import settings
from user.models import User
from versatileimagefield.serializers import VersatileImageFieldSerializer
from user.utils.token_generators import _OTPVerifyTokenGenerator


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


class TokenCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed({'message': 'User not found'})

        if not user.check_password(password):
            raise AuthenticationFailed({'message': 'Incorrect password'})

        update_last_login(None, user)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return {
            'refresh': str(refresh),
            'access': str(access),
            'user': UserRetrieveSerializer(user).data,
        }


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68,
        min_length=6,
        write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=68,
        min_length=6,
        write_only=True
    )

    def create(self, validated_data):
        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')
        validated_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.set_password(password)
        user.save()

        token = _OTPVerifyTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(str(user.id).encode())
        data = {
            'user': user,
            'url': f'{settings.FRONTEND_URL}/user/activate-account/{uid}/{token}',
            'uid': uid,
            'token': token,
        }
        send_mail(
            subject='This is a email for account activation',
            message=render_to_string('auth/activate_email.html', data),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return user

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'confirm_password',
        )
