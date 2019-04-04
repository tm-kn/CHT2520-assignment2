from django.urls import path

from timetracker.sheets.views import TimeSheetListView

app_name = 'sheets'

urlpatterns = [
    path('', TimeSheetListView.as_view(), name='list'),
]
