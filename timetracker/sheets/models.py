from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeSheet(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.PROTECT,
        related_name='timesheets',
        verbose_name=_('user'))

    class Meta:
        verbose_name = _('time sheet')
        verbose_name_plural = _('time sheets')

    def __str__(self):
        return self.title
