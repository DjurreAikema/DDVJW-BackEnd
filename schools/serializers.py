from rest_framework.serializers import ModelSerializer
from .models import School


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'email', 'phone_number', 'address', 'zip_code']
