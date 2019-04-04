from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from timetracker.sheets.models import TimeSheet


class TimeSheetListView(LoginRequiredMixin, ListView):
    """
    List user's time sheets.
    """
    model = TimeSheet

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
