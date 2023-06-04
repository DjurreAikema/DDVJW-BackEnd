from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from core.authentication import decode_access_token
from core.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            user_id = decode_access_token(token)

            return User.objects.get(pk=user_id), None

        raise exceptions.AuthenticationFailed('Unauthenticated')
