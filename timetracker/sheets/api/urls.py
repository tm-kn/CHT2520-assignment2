from django.urls import path

from timetracker.sheets.api.views import HoursPerProjectStatisticsView, TimeSheetListView

app_name = 'sheets'

urlpatterns = [
    path(
        '<int:sheet_pk>/hours-per-project-statistics/',
        HoursPerProjectStatisticsView.as_view(),
        name='hours-per-project-statistics'),
    path('', TimeSheetListView.as_view(), name='root'),
]
