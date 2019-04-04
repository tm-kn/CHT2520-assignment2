import io
import logging
from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from timetracker.sheets.csv import generate_timesheet_csv

logger = logging.getLogger(__name__)


class TimeSheetGeneratedFile(models.Model):
    sheet = models.ForeignKey(
        'TimeSheet',
        models.CASCADE,
        related_name='files',
        verbose_name=_('sheet'))
    file = models.FileField(
        verbose_name=_('file'), upload_to='timesheet_exports')
    generated_at = models.DateTimeField(
        default=timezone.now, verbose_name=_('generated at'))

    class Meta:
        verbose_name = _('time sheet file')
        verbose_name_plural = _('time sheet files')

    def can_access_file(self, request):
        return request.user == self.sheet.user

    def get_absolute_url(self):
        return reverse(
            'sheets:exported_file',
            kwargs={
                'sheet_pk': self.sheet_id,
                'pk': self.pk,
            })

    def send_email_with_file_link(self):
        user = self.sheet.user
        file_link = urljoin(settings.BASE_URL, self.get_absolute_url())
        send_mail(
            'Exported time sheet download link',
            (f'Hi {user},\n\n'
             'The link to your generated CSV time sheet file is:\n'
             f'{file_link}'),
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )


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

    def get_absolute_url(self):
        """
        Get a URL to the detail page of this time sheet.
        """
        return reverse('activities:list', kwargs={'sheet_pk': self.pk})

    def generate_csv_file(self, end_datetime=None):
        activities = self.activities.filter(end_datetime__isnull=False)

        if end_datetime is not None:
            activities = activities.filter(end_datetime__lte=end_datetime)
        buffer_object = io.StringIO()
        filename = f'timesheet-{self.pk}-{slugify(self.title)}' \
                   f'-{slugify(end_datetime or timezone.now())}.csv'
        generate_timesheet_csv(buffer_object, self, activities)
        generated_file = TimeSheetGeneratedFile(sheet=self)
        generated_file.file.save(
            filename, ContentFile(buffer_object.getvalue().encode('utf-8')))
        generated_file.save()
        logger.info('Generated timesheet file "%s"', filename)
        generated_file.send_email_with_file_link()
