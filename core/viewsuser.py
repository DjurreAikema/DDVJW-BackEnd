from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.middleware import JWTAuthentication
from core.models import User
from core.permissions import CanViewUserList, CanViewUserDetails, CanCreateUser, CanUpdateUser, CanDeleteUser
from core.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes_by_action = {
        'list': [IsAuthenticated, CanViewUserList],
        'retrieve': [IsAuthenticated, CanViewUserDetails],
        'create': [IsAuthenticated, CanCreateUser],
        'update': [IsAuthenticated, CanUpdateUser],
        'destroy': [IsAuthenticated, CanDeleteUser],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return super().get_permissions()
