from django.urls import path
from timetracker.api.views import root


urlpatterns = [
    path('', root, name='root'),
]
