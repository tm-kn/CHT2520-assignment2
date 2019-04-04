from django.db import models
from django.utils.translation import ugettext_lazy as _


class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    sheet = models.ForeignKey(
        'sheets.TimeSheet',
        models.PROTECT,
        related_name='projects',
        verbose_name=_('time sheet'))

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __str__(self):
        return self.name
