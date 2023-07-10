from django.db import models

from core.models import User


class Report(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_trainer')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_client')
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title
