from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from ckeditor_uploader.fields import RichTextUploadingField
from djangoProject.utils.custom_fields import CustomVersatileImageField


# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    first_name = models.CharField(verbose_name=_('first name'), max_length=50)
    last_name = models.CharField(verbose_name=_('last name'), max_length=50)
    profile_picture = CustomVersatileImageField(
        verbose_name=_('profile picture'),
        upload_to='profile_pictures',
    )
    order = models.PositiveIntegerField(verbose_name=_('order'), default=0, blank=True, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('order',)

    def set_active(self):
        self.is_active = True
        self.save(update_fields=['is_active'])

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def hidden_email(self):
        return self.email[:3] + '*' * (len(self.email[:-10]) - 3) + '@' + self.email.split('@')[1]



    def __str__(self):
        return self.email