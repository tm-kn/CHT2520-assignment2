from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SheetsConfig(AppConfig):
    name = 'timetracker.sheets'
    verbose_name = _('Sheets')

    def ready(self):
        from timetracker.sheets.signals import register_signals
        register_signals()
