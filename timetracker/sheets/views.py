from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from timetracker.sheets.forms import TimeSheetForm
from timetracker.sheets.models import TimeSheet


class CurrentUserTimeSheetQuerySetMixin:
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TimeSheetListView(LoginRequiredMixin, CurrentUserTimeSheetQuerySetMixin,
                        ListView):
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


class TimeSheetDeleteView(LoginRequiredMixin,
                          CurrentUserTimeSheetQuerySetMixin, DeleteView):
    """
    Delete a time sheet  object.
    """
    model = TimeSheet

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        with transaction.atomic():
            self.object.activities.all().delete()
            response = super().delete(request, *args, **kwargs)
        messages.success(self.request, _('Successfully deleted a time sheet.'))
        return response

    def get_success_url(self):
        return reverse('sheets:list')
