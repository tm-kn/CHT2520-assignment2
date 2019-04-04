from django.urls import path

from timetracker.sheets.views import TimeSheetCreateView, TimeSheetListView

app_name = 'sheets'

urlpatterns = [
    path('', TimeSheetListView.as_view(), name='list'),
    path('create/', TimeSheetCreateView.as_view(), name='create'),
]
