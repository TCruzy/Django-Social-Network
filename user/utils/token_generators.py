from django.contrib.auth.tokens import PasswordResetTokenGenerator


class _OTPVerifyTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        hash_value = super()._make_hash_value(user, timestamp)
        return f'{hash_value}{user.is_active}'
