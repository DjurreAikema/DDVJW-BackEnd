from rest_framework.serializers import ModelSerializer
from .models import User


# Serializers convert Django models into another format. In this case we convert a Django model to json.
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
