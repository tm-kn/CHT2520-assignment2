from django.urls import path

from timetracker.sheets.api.views import PerProjectStatisticsView, sheets_root

app_name = 'sheets'

urlpatterns = [
    path(
        'per-project-statistics/',
        PerProjectStatisticsView.as_view(),
        name='per-project-statistics'),
    path('', sheets_root, name='root'),
]
