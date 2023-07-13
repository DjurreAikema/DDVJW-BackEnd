from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User


# Serializers convert Django models into another format. In this case we convert a Django model to json.
class UserSerializer(ModelSerializer):
    school_name = serializers.CharField(max_length=255, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'school', 'school_name', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['school']:
            representation['school_name'] = instance.school.name

        return representation

    def create(self, validated_data):
        # Extract the password
        password = validated_data.pop('password', None)
        # Create the user
        instance = self.Meta.model(**validated_data)

        # Hash the password and set in on the user
        if password is not None:
            instance.set_password(password)

        # Save the user
        instance.save()
        return instance
