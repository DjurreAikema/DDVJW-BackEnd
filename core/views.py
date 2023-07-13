import datetime
import random
import string

from django.core.mail import send_mail
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentication import create_access_token, create_refresh_token, decode_refresh_token
from core.middleware import JWTAuthentication
from core.models import User, UserToken, ResetPassword
from core.serializers import UserSerializer


# class RegisterAPIView(APIView):
#     def post(self, request):
#         try:
#             data = request.data
#
#             # Check if password and password_confirm fields match
#             if data['password'] != data['password_confirm']:
#                 raise exceptions.APIException('Passwords do not match')
#
#             # Instantiate the serializer with the request data
#             serializer = UserSerializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#
#         except Exception as e:
#             return Response({
#                 'message': 'An error occurred: {}'.format(e)
#             })
#
#         return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        try:
            # Get email and password from request data
            email = request.data['email']
            password = request.data['password']

            # Retrieve the user with the given email
            user = User.objects.filter(email=email).first()

            # Raise an AuthenticationFailed exception if the user is not found
            if user is None:
                raise exceptions.AuthenticationFailed('Invalid credentials')

            # Raise an AuthenticationFailed exception if the password is invalid
            if not user.check_password(password):
                raise exceptions.AuthenticationFailed('Invalid credentials')

            # Create access and refresh tokens
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)

            # Save the refresh token
            UserToken.objects.create(
                user_id=user.id,
                token=refresh_token,
                expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=7)
            )

            # Create a response object
            response = Response()
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
            response.data = {
                'token': access_token
            }

        except Exception as e:
            return Response({
                'message': 'An error occurred: {}'.format(e)
            })

        return response


class RefreshAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            if refresh_token is None:
                raise exceptions.AuthenticationFailed('Unauthenticated')

            user_id = decode_refresh_token(refresh_token)

            # Check if the refresh token is valid
            if not UserToken.objects.filter(
                    user_id=user_id,
                    token=refresh_token,
                    expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)
            ).exists():
                raise exceptions.AuthenticationFailed('Unauthenticated')

            # Create a new access token
            access_token = create_access_token(user_id)

        except Exception as e:
            return Response({
                'message': 'An error occurred: {}'.format(e)
            })

        return Response({
            'token': access_token
        })


class LogoutAPIView(APIView):

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            UserToken.objects.filter(token=refresh_token).delete()

        except Exception as e:
            return Response({
                'message': 'An error occurred: {}'.format(e)
            })

        # Create a response object and delete the refresh_token cookie
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message': 'success'
        }

        return response


class ForgotAPIView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            # Generate a random token
            token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))

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

        except Exception as e:
            return Response({
                'message': 'An error occurred: {}'.format(e)
            })

        return Response({
            'message': 'success'
        })


class ResetAPIView(APIView):
    def post(self, request):
        try:
            data = request.data

            # Check if the password and password confirmation match
            if data['password'] != data['password_confirm']:
                raise exceptions.APIException('Passwords do not match')

            reset_password = ResetPassword.objects.filter(token=data['token']).first()

            # Return an error if the reset password object is not found
            if not reset_password:
                raise exceptions.APIException('Invalid link')

            user = User.objects.filter(email=reset_password.email).first()

            # Return an error if the user is not found
            if not user:
                raise exceptions.APIException('User not found')

            # Set the user's password to the new password
            user.set_password(data['password'])
            user.save()

            # Delete the reset password object
            reset_password.delete()

        except Exception as e:
            return Response({
                'message': 'An error occurred: {}'.format(e)
            })

        return Response({
            'message': 'success'
        })


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            serialized_user = UserSerializer(request.user).data

        except Exception as e:
            return Response({
                'message': 'An error occurred: {}'.format(e)
            })

        return Response(serialized_user)
