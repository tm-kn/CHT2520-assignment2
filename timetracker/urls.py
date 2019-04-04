from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from timetracker.home.views import HomepageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('timetracker.accounts.urls')),
    path('sheets/', include('timetracker.sheets.urls')),
    path('sheets/<int:sheet_pk>/',
         include('timetracker.activities.urls', namespace='activities')),
    path('', HomepageView.as_view(), name='home')
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
