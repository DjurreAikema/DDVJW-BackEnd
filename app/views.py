from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # 'api-auth': reverse('api-auth', request=request, format=format),
        # 'schools': reverse('school-list', request=request, format=format),
        # 'reports': reverse('report-list', request=request, format=format)
    })
