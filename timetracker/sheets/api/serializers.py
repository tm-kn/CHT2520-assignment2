from django.utils import timezone

from rest_framework import serializers

from timetracker.sheets.models import TimeSheet


class TimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet


class PerProjectStatisticsSerializer(TimeSheetSerializer):
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()

    def get_start_date(self, obj):
        # Get Monday
        return timezone.now().date() - timezone.timedelta(
            days=timezone.now().weekday())

    def get_end_date(self, obj):
        return self.get_start_date(obj) + timezone.timedelta(days=6)

    def get_activities(self, obj):
        days = []
        date = self.get_start_date(obj)

        while date <= self.get_end_date(obj):
            next_day = date + timezone.timedelta(days=1)
            activities = obj.activities.filter(
                start_datetime__gte=date,
                start_datetime__lt=next_day,
            ).select_related('project')
            projects = {}
            for activity in activities:
                if activity.project_id not in projects:
                    projects[activity.project_id] = {
                        'title': activity.project.name,
                        'date': date,
                        'duration_seconds': 0,
                    }
                projects[activity.project_id]['duration_seconds'] += (
                    activity.duration.seconds)
            days.append({
                'date': date,
                'projects': projects,
            })
            date = next_day
        return days

    class Meta(TimeSheetSerializer.Meta):
        fields = (
            'start_date',
            'end_date',
            'activities',
        )
