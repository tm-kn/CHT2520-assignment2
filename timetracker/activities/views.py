from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.detail import (DetailView, SingleObjectMixin,
                                         SingleObjectTemplateResponseMixin)
from django.views.generic.edit import BaseUpdateView, CreateView, DeleteView
from django.views.generic.list import ListView

from timetracker.activities.forms import ActivityFilterForm, ActivityForm
from timetracker.activities.models import Activity
from timetracker.sheets.views import CurrentSheetMixin


class ActivityQuerySetMixin(CurrentSheetMixin):
    """
    Constraint queryset to return activities only created by the
    current user in the selected sheet.
    """
    model = Activity

    def get_queryset(self):
        return super().get_queryset().filter(
            sheet_id=self.kwargs['sheet_pk'],
            sheet__user_id=self.request.user.pk).select_related('sheet')


class ActivitySingleObjectMixin(ActivityQuerySetMixin, SingleObjectMixin):
    """
    Get SingleObjectMixin with constraints of ActivityQuerysetMixin.
    """
    pass


class ActivityCreateView(CurrentSheetMixin, LoginRequiredMixin, CreateView):
    """
    Create a new activity.
    """
    form_class = ActivityForm
    template_name = 'activities/activity_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'sheet': self.get_sheet()})
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Successfully created an activity.'))
        return response

    def get_success_url(self):
        return reverse(
            'activities:list', kwargs={'sheet_pk': self.get_sheet().pk})


class ActivityListView(LoginRequiredMixin, ActivityQuerySetMixin, ListView):
    """
    List and search the activities.
    """

    def get_queryset(self):
        start_of_range = self.filter_form.cleaned_data.get('start_date')
        end_of_range = self.filter_form.cleaned_data.get('end_date')
        qs = super().get_queryset()
        if start_of_range and end_of_range:
            if start_of_range > end_of_range:
                start_of_range, end_of_range = end_of_range, start_of_range
            start_of_range = timezone.datetime.combine(
                start_of_range, timezone.datetime.min.time())
            end_of_range = timezone.datetime.combine(
                end_of_range, timezone.datetime.max.time())
            qs &= super().get_queryset().filter(
                start_datetime__gte=start_of_range,
                start_datetime__lte=end_of_range)

        search_query = self.filter_form.cleaned_data['search_query']
        if search_query:
            # Search query using Postgres full-text search.
            qs &= super().get_queryset().annotate(
                search=SearchVector(
                    'activity', 'project',
                    'description'), ).filter(search=search_query)
        return qs

    def get_filter_form(self):
        """
        Get a form object of the filters.
        """
        filter_form_data = self.request.GET.copy()
        filter_form_data.setdefault(
            'start_date',
            timezone.now().date() - timezone.timedelta(days=7))
        filter_form_data.setdefault('end_date', timezone.now().date())
        return ActivityFilterForm(filter_form_data)

    def get(self, request, *args, **kwargs):
        # Initialise filter form on the get request.
        self.filter_form = self.get_filter_form()
        self.filter_form.is_valid()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter form to the template context so it can be
        # rendered on the index template.
        context['filter_form'] = self.filter_form
        return context


class ActivityDetailView(LoginRequiredMixin, ActivitySingleObjectMixin,
                         DetailView):
    """
    Display information about singular activity.
    """
    pass


class ActivityUpdateView(LoginRequiredMixin, ActivitySingleObjectMixin,
                         SingleObjectTemplateResponseMixin, BaseUpdateView):
    """
    Update an existing activity.
    """
    form_class = ActivityForm
    template_name = 'activities/activity_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'sheet': self.get_sheet()})
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Successfully updated an activity.'))
        return response


class ActivityStopView(ActivitySingleObjectMixin, View):
    """
    Stop an active activity.
    """

    def post(self, *args, **kwargs):
        obj = self.get_object()
        obj.stop()
        messages.success(self.request, _('Successfully stopped an activity.'))
        return redirect('activities:list', sheet_pk=obj.sheet_id)


class ActivityDeleteView(ActivitySingleObjectMixin, DeleteView):
    """
    Delete an activity object.
    """

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, _('Successfully deleted an activity'))
        return response

    def get_success_url(self):
        return reverse(
            'activities:list', kwargs={'sheet_pk': self.get_sheet().pk})
