from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 1
    TRAINER = 2
    CLIENT = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (TRAINER, 'Trainer'),
        (CLIENT, 'Client')
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=False, null=False, default=CLIENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()


class ResetPassword(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=20, unique=True)
