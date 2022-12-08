from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from user.utils.token_generators import OTPVerifyTokenGenerator


class HasValidOTPToken(BasePermission):
    """
    Allows access only to user with Valid OTP Token.
    """

    def has_permission(self, request, view):
        if not OTPVerifyTokenGenerator.check_token(view.object, view.kwargs.get('token')):
            raise PermissionDenied(code=status.HTTP_403_FORBIDDEN)
        return True


class HasValidRecoverToken(BasePermission):
    """
    Allows access only to user with Valid Recover Token.
    """

    def has_permission(self, request, view):
        if not default_token_generator.check_token(view.object, view.kwargs.get('token')):
            raise PermissionDenied(code=status.HTTP_403_FORBIDDEN)
        return True



