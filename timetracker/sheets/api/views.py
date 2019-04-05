from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.generics import RetrieveAPIView

from timetracker.sheets.models import TimeSheet
from timetracker.sheets.api.serializers import PerProjectStatisticsSerializer


@api_view(['GET'])
def sheets_root(request):
    return Response({
        'per-project-statistics':
        reverse('api:sheets:per-project-statistics', request=request),
    })


class PerProjectStatisticsView(RetrieveAPIView):
    lookup_url_kwarg = 'sheet_pk'
    serializer_class = PerProjectStatisticsSerializer

    def get_queryset(self):
        return TimeSheet.objects.filter(user_id=self.request.user)
