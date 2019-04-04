from django.urls import path

from timetracker.projects.views import ProjectCreateView

app_name = 'projects'

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='create'),
]
