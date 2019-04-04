from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.generic import View
from django.views.generic.detail import (DetailView, SingleObjectMixin,
                                         SingleObjectTemplateResponseMixin)
from django.views.generic.edit import BaseUpdateView, CreateView, DeleteView
from django.views.generic.list import ListView

from timetracker.sheets.forms import TimeSheetForm
from timetracker.sheets.models import TimeSheet, TimeSheetGeneratedFile
from timetracker.sheets.tasks import generate_csv_file_for_timesheet


class CurrentSheetMixin:
    def get_sheet(self):
        try:
            return TimeSheet.objects.get(
                pk=self.kwargs['sheet_pk'], user=self.request.user)
        except TimeSheet.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sheet'] = self.get_sheet()
        return context


class CurrentUserTimeSheetQuerySetMixin:
    model = TimeSheet

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


class TimeSheetUpdateView(LoginRequiredMixin,
                          CurrentUserTimeSheetQuerySetMixin,
                          SingleObjectTemplateResponseMixin, BaseUpdateView):
    form_class = TimeSheetForm
    template_name = 'sheets/timesheet_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,
                         _('Successfully created a new time-sheet.'))
        return response


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
            self.object.projects.all().delete()
            response = super().delete(request, *args, **kwargs)
        messages.success(self.request, _('Successfully deleted a time sheet.'))
        return response

    def get_success_url(self):
        return reverse('sheets:list')


class TimeSheetExportView(LoginRequiredMixin,
                          CurrentUserTimeSheetQuerySetMixin, DetailView):
    template_name = 'sheets/timesheet_export.html'

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        generate_csv_file_for_timesheet.delay(self.object.pk, timezone.now())
        messages.success(
            self.request,
            _('File queued for generation. Check your e-mail '
              'for a link to a file.'))
        return redirect('activities:list', sheet_pk=self.object.pk)


class TimeSheetGeneratedFileView(LoginRequiredMixin, CurrentSheetMixin,
                                 SingleObjectMixin, View):
    model = TimeSheetGeneratedFile

    def get_queryset(self):
        return super().get_queryset().filter(sheet_id=self.get_sheet().pk)

    @never_cache
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_access_file(request):
            raise Http404
        return redirect(self.object.file.url)
