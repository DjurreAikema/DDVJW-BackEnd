from rest_framework.viewsets import ModelViewSet

from core.middleware import JWTAuthentication
from schools.models import School
from schools.permissions import CanViewSchoolList, CanViewSchoolDetails, CanCreateSchool, CanUpdateSchool, CanDeleteSchool
from schools.serializers import SchoolSerializer


class SchoolViewSet(ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes_by_action = {
        'list': [CanViewSchoolList],
        'retrieve': [CanViewSchoolDetails],
        'create': [CanCreateSchool],
        'update': [CanUpdateSchool],
        'destroy': [CanDeleteSchool],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return super().get_permissions()
