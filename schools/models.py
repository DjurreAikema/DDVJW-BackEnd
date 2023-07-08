from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=6)
