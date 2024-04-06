from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from pytz import timezone

from .managers import CustomUserManager
from .token_generators import generate_jwt


# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    email = models.EmailField(verbose_name='email', unique=True)
    is_staff = models.BooleanField(default=False, verbose_name='Administrator')

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def access_token(self):
        return generate_jwt(self.pk)


class RefreshToken(models.Model):
    token = models.CharField(max_length=255)
    expires = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.expires = datetime.now(timezone(settings.TIME_ZONE)) + timedelta(**settings.REFRESH_TOKEN_LIFETIME)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.token


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, default='', blank=True)
    last_name = models.CharField(max_length=32, default='', blank=True)
    title = models.CharField(max_length=32, default='', blank=True)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True, default=None)
    friends = models.ManyToManyField('self', blank=True, through='Friend')


class Friend(models.Model):
    first = models.ForeignKey(Profile, on_delete=models.CASCADE)
    second = models.ForeignKey(Profile, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
