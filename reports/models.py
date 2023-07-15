from django.db import models

from core.models import User


class Report(models.Model):
    title = models.CharField(max_length=255)

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_client')
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_trainer')

    def __str__(self) -> str:
        return self.title
