from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from core.middleware import JWTAuthentication
from reports.models import Report
from reports.permissions import CanViewReportList, CanViewReportDetails, CanCreateReport, CanUpdateReport, CanDeleteReport
from reports.serializers import ReportSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'reports': reverse('report-list', request=request, format=format)
    })


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes_by_action = {
        'list': [CanViewReportList],
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
