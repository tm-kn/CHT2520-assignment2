from collections import OrderedDict

from django.utils import timezone

from rest_framework import serializers

from timetracker.sheets.models import TimeSheet


class TimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet


class PerProjectStatisticsSerializer(TimeSheetSerializer):
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    days = serializers.SerializerMethodField()

    def get_start_date(self, obj):
        # Get Monday
        return timezone.now().date() - timezone.timedelta(
            days=timezone.now().weekday())

    def get_end_date(self, obj):
        return self.get_start_date(obj) + timezone.timedelta(days=6)

    def get_days(self, obj):
        date = self.get_start_date(obj)
        while date <= self.get_end_date(obj):
            yield date
            date += timezone.timedelta(days=1)

    def get_projects(self, obj):
        projects = {}
        date = self.get_start_date(obj)

        while date <= self.get_end_date(obj):
            next_day = date + timezone.timedelta(days=1)
            activities = obj.activities.filter(
                start_datetime__gte=date,
                start_datetime__lt=next_day,
            ).select_related('project')
            for activity in activities:
                if activity.project_id not in projects:
                    projects[activity.project_id] = {
                        'id': activity.project_id,
                        'title': activity.project.name,
                        'days': OrderedDict(),
                    }
                for day in self.get_days(obj):
                    if day.isoformat() not in projects[
                            activity.project_id]['days']:
                        projects[activity.project_id]['days'][
                            day.isoformat()] = {
                                'date': day.isoformat(),
                                'duration_seconds': 0
                            }

                projects[activity.project_id]['days'][date.isoformat(
                )]['duration_seconds'] += (activity.duration.seconds)
            date = next_day

        for project in projects.values():
            project['days'] = project['days'].values()
        return projects.values()

    class Meta(TimeSheetSerializer.Meta):
        fields = (
            'start_date',
            'end_date',
            'days',
            'projects',
        )
