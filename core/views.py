from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User
from core.serializers import UserSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match')

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid credentials')

        serializer = UserSerializer(user)
        return Response(serializer.data)
