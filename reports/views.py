from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from reports.models import Report
from reports.permissions import CanViewReportList, CanViewReportDetails, CanCreateReport, CanUpdateReport, CanDeleteReport
from reports.serializers import ReportSerializer


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes_by_action = {
        'list': [IsAuthenticated, CanViewReportList],
        'retrieve': [IsAuthenticated, CanViewReportDetails],
        'create': [IsAuthenticated, CanCreateReport],
        'update': [IsAuthenticated, CanUpdateReport],
        'partial_update': [IsAuthenticated, CanUpdateReport],
        'destroy': [IsAuthenticated, CanDeleteReport],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return super().get_permissions()
