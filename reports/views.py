from rest_framework.viewsets import ModelViewSet

from core.middleware import JWTAuthentication
from reports.models import Report
from reports.permissions import CanViewReportList, CanViewReportDetails, CanCreateReport, CanUpdateReport, CanDeleteReport
from reports.serializers import ReportSerializer


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes_by_action = {
        'list': [CanViewReportList],
        'retrieve': [CanViewReportDetails],
        'create': [CanCreateReport],
        'update': [CanUpdateReport],
        'partial_update': [CanUpdateReport],
        'destroy': [CanDeleteReport],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return super().get_permissions()
