from django.contrib.auth.models import AbstractUser
from django.db import models

from schools.models import School


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('trainer', 'Trainer'),
        ('client', 'Client')
    )

    username = None
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, blank=False, null=False, default='client')

    trainer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, related_name='school', null=True, blank=True)

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
