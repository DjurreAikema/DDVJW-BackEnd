# Generated by Django 4.2.3 on 2023-07-15 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='report',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
