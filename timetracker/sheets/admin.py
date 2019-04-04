from django.contrib import admin

from timetracker.sheets.models import TimeSheet


@admin.register(TimeSheet)
class TimeSheetAdmin(admin.ModelAdmin):
    list_filter = ('user', )
    search_fields = ('title', )
