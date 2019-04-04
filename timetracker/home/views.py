from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView


class HomepageView(LoginRequiredMixin, RedirectView):
    """
    Redirect to activities list if user is logged in.

    If user is not logged in, redirect to the default login page.
    """
    pattern_name = 'sheets:list'
