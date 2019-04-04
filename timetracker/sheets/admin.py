from django.contrib import admin

from timetracker.sheets.models import TimeSheet, TimeSheetGeneratedFile


class TimeSheetGeneratedFileInline(admin.TabularInline):
    model = TimeSheetGeneratedFile

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(TimeSheet)
class TimeSheetAdmin(admin.ModelAdmin):
    list_filter = ('user', )
    search_fields = ('title', )
    inlines = (TimeSheetGeneratedFileInline, )
