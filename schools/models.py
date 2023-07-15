from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
