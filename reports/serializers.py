from rest_framework.serializers import ModelSerializer

from reports.models import Report


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'trainer', 'client', 'title', 'completed', 'visible_to_client', 'created']
