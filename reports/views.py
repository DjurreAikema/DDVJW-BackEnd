from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
        'list': [IsAuthenticated, CanViewReportList],
        'retrieve': [IsAuthenticated, CanViewReportDetails],
        'create': [IsAuthenticated, CanCreateReport],
        'update': [IsAuthenticated, CanUpdateReport],
        'partial_update': [IsAuthenticated, CanUpdateReport],
        'destroy': [IsAuthenticated, CanDeleteReport],
    }

    @action(detail=True)
    def get_active_report(self, request, pk):
        report = Report.objects.filter(client=pk, completed=False).first()
        if not report:
            return Response({'message': 'no active report'})

        serializer = self.get_serializer(report, many=False)
        return Response(serializer.data)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return super().get_permissions()
