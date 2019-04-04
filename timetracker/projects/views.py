from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.urls import reverse
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView

from timetracker.sheets.views import CurrentSheetMixin
from timetracker.projects.forms import ProjectForm


class ProjectCreateView(CurrentSheetMixin, LoginRequiredMixin,
                        SuccessURLAllowedHostsMixin, CreateView):
    """
    Create a new project for a given sheet.
    """
    form_class = ProjectForm
    template_name = 'projects/project_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'sheet': self.get_sheet()})
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Successfully created a project.'))
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.get_next_url(self.request.GET)
        return context

    def get_success_url(self):
        next_url = self.get_next_url(self.request.POST)
        if next_url is not None:
            return next_url
        return reverse(
            'activities:list', kwargs={'sheet_pk': self.get_sheet().pk})

    def get_next_url(self, data):
        try:
            redirect_to = data['next']
            if is_safe_url(
                    redirect_to,
                    allowed_hosts=self.get_success_url_allowed_hosts(),
                    require_https=self.request.is_secure()):
                return redirect_to
        except KeyError:
            return
