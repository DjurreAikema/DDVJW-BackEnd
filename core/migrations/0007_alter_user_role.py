# Generated by Django 4.2.1 on 2023-07-10 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('trainer', 'Trainer'), ('client', 'Client')], default='client', max_length=7),
        ),
    ]