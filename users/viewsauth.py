import random
import string

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import ResetPassword, User
from users.serializers import UserSerializer, LoginSerializer, PasswordForgotSerializer, ResetPasswordSerializer, RegisterSerializer


class UserAuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    # --- Register
    @action(detail=False, methods=['post'], serializer_class=RegisterSerializer)
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user_serializer = UserSerializer(data=serializer.validated_data)

            if user_serializer.is_valid():
                user_serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- Login
    @action(detail=False, methods=['post'], serializer_class=LoginSerializer)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Get the user object from authentication
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])

            # Generate access and refresh tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Set the refresh token in an HTTP-only cookie
            response = HttpResponse()
            response.set_cookie(key='refresh_token', value=str(refresh), httponly=True)
            response.data = {'access_token': access_token}

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- Logout
    @action(detail=False, methods=['post'])
    def logout(self):
        response = HttpResponse()
        response.delete_cookie('refresh_token')
        response.data = {'message': 'Logout successful'}

        return response

    # --- Password forgot
    @action(detail=False, methods=['post'], serializer_class=PasswordForgotSerializer)
    def password_forgot(self, request):
        serializer = PasswordForgotSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']

            # Generate a random token
            token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))

            # Delete previous reset token(s) for the same email
            ResetPassword.objects.filter(email=email).delete()

            # Create a new reset password object
            ResetPassword.objects.create(
                email=email,
                token=token
            )

            # Create link to the front-end where the user can fill in a new password
            url = 'http://localhost:4200/reset/' + token

            # Send the reset password email
            send_mail(
                subject='Reset your password',
                message='Click <a href="%s">here</a> to reset your password' % url,
                from_email='from@example.com',
                recipient_list=[email]
            )

            return Response({'message': 'Password reset instructions sent'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- Password reset
    @action(detail=False, methods=['post'], serializer_class=ResetPasswordSerializer)
    def password_reset(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            try:
                reset_obj = ResetPassword.objects.get(token=token)
            except ResetPassword.DoesNotExist:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's password
            user = User.objects.filter(email=reset_obj.email).first()
            user.set_password(new_password)
            user.save()

            # Delete the reset token
            reset_obj.delete()

            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
