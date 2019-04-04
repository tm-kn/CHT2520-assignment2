from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from timetracker.sheets.models import TimeSheet
from timetracker.sheets.forms import TimeSheetForm


class TimeSheetListView(LoginRequiredMixin, ListView):
    """
    List user's time sheets.
    """
    model = TimeSheet

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class TimeSheetCreateView(LoginRequiredMixin, CreateView):
    form_class = TimeSheetForm
    template_name = 'sheets/timesheet_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,
                         _('Successfully created a new time-sheet.'))
        return response

    def get_success_url(self):
        return self.object.get_absolute_url()
