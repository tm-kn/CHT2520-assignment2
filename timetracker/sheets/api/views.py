from rest_framework.reverse import reverse

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def sheets_root(request):
    return Response({
        'per-project-statistics':
        reverse('api:sheets:per-project-statistics', request=request),
    })


class PerProjectStatisticsView(APIView):
    pass
