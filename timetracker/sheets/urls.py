from django.urls import path

from timetracker.sheets.views import (TimeSheetCreateView, TimeSheetDeleteView,
                                      TimeSheetListView)

app_name = 'sheets'

urlpatterns = [
    path('', TimeSheetListView.as_view(), name='list'),
    path('create/', TimeSheetCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', TimeSheetDeleteView.as_view(), name='delete'),
]
