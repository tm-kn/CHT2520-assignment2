from django.urls import include, path

from timetracker.api.views import root

app_name = 'api'

urlpatterns = [
    path('v1/', include([
        path('sheets/', include('timetracker.sheets.api.urls')),
        path('', root, name='root'),
    ])),
]
