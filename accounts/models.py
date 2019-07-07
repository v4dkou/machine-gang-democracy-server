from django.utils import timezone

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        user = self.model(username=username, **kwargs)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **kwargs):
        return self.create_user(
            username,
            password,
            is_staff=True,
            is_active=True,
            is_superuser=True,
            **kwargs
        )

    def create_email_user(self, email, password, **kwargs):
        return self.create_user(email, password, email=email, **kwargs)

    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)


class User(PermissionsMixin, AbstractBaseUser):
    username = models.CharField("Username", max_length=160, unique=True)
    email = models.EmailField("Email address", max_length=100)

    fullname = models.CharField('Full name', max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)

    is_staff = models.BooleanField("Admin", default=False)
    is_active = models.BooleanField("Active user", default=False)

    date_joined = models.DateTimeField("Date joined", default=timezone.now, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class UserSession(models.Model):
    user = models.ForeignKey(User, verbose_name='User', related_name='sessions', on_delete=models.CASCADE)
    token = models.CharField('Token', max_length=64)

    ip_address = models.CharField('IP address', max_length=32, blank=True, null=True)
    user_agent = models.CharField('User agent', max_length=255, blank=True, null=True)

    date_created = models.DateTimeField('Created', default=timezone.now, editable=False)
