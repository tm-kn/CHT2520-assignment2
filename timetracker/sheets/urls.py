from django.urls import path

# yapf: disable
from timetracker.sheets.views import (TimeSheetCreateView, TimeSheetDeleteView,
                                      TimeSheetExportView,
                                      TimeSheetGeneratedFileView,
                                      TimeSheetListView, TimeSheetUpdateView)

# yapf: enable

app_name = 'sheets'

urlpatterns = [
    path('', TimeSheetListView.as_view(), name='list'),
    path('create/', TimeSheetCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', TimeSheetDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', TimeSheetUpdateView.as_view(), name='update'),
    path('<int:pk>/export/', TimeSheetExportView.as_view(), name='export'),
    path(
        '<int:sheet_pk>/exported-file/<int:pk>/',
        TimeSheetGeneratedFileView.as_view(),
        name='exported_file'),
]
