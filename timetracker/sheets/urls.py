from django.urls import path

from timetracker.sheets.views import (TimeSheetCreateView, TimeSheetDeleteView,
                                      TimeSheetExportView, TimeSheetListView,
                                      TimeSheetUpdateView)

app_name = 'sheets'

urlpatterns = [
    path('', TimeSheetListView.as_view(), name='list'),
    path('create/', TimeSheetCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', TimeSheetDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', TimeSheetUpdateView.as_view(), name='update'),
    path('<int:pk>/export/', TimeSheetExportView.as_view(), name='export'),
]
