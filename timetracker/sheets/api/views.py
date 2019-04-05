from rest_framework.generics import ListAPIView, RetrieveAPIView

from timetracker.sheets.models import TimeSheet

from timetracker.sheets.api.serializers import (  # isort:skip
    HoursPerProjectStatisticsSerializer, TimeSheetSerializer)


class TimeSheetListView(ListAPIView):
    serializer_class = TimeSheetSerializer

    def get_queryset(self):
        return TimeSheet.objects.filter(user_id=self.request.user)


class HoursPerProjectStatisticsView(RetrieveAPIView):
    lookup_url_kwarg = 'sheet_pk'
    serializer_class = HoursPerProjectStatisticsSerializer

    def get_queryset(self):
        return TimeSheet.objects.filter(user_id=self.request.user)
