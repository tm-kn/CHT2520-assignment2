from django.contrib import admin

from timetracker.activities.models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_filter = ('user', )
    search_fields = (
        'project',
        'activity',
        'description',
    )
