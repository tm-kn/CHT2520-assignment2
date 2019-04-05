from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from timetracker.accounts.forms import RegistrationForm


class RegistrationView(CreateView):
    model = get_user_model()
    form_class = RegistrationForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        # User already logged in
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, form.instance)
        return response
