import random
import string

from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User, ResetPassword


# Serializers convert Django models into another format. In this case we convert a Django model to json.
class UserSerializer(ModelSerializer):
    school_name = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, default='Geen school')
    trainer_name = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, default='Geen trainer')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'school', 'school_name', 'trainer', 'trainer_name', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation['school']:
            representation['school_name'] = instance.school.name

        if representation['trainer']:
            representation['trainer_name'] = instance.trainer.first_name + ' ' + instance.trainer.last_name

        return representation


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'school', 'trainer', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)

        # Generate a random password for the user
        password = get_random_string(10)
        instance.set_password(password)

        # Save the user
        instance.save()

        # Send a password reset email to the email used to create the user
        email = validated_data.pop('email', None)
        if email is not None:
            send_reset_password_email(email)

        return instance


def send_reset_password_email(email):
    token = get_random_string(20)

    # TODO Delete previous reset token when asking for a new one
    # Create a new reset password object
    ResetPassword.objects.create(
        email=email,
        token=token
    )

    url = 'http://localhost:4200/reset/' + token

    # Send the reset password email
    send_mail(
        subject='Reset your password',
        message='Click <a href="%s">here</a> to reset your password' % url,
        from_email='from@example.com',
        recipient_list=[email]
    )


def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
