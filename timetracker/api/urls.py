from django.urls import include, path
from timetracker.api.views import root

app_name = 'api'

urlpatterns = [
    path('sheets/', include('timetracker.sheets.api.urls')),
    path('', root, name='root'),
]
