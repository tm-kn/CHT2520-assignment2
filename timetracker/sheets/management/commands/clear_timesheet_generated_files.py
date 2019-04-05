import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from timetracker.sheets.models import TimeSheetGeneratedFile

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Delete old time sheet generated files (older than 7 days)'

    def handle(self, *args, **options):
        files = TimeSheetGeneratedFile.objects.filter(
            generated_at__lte=timezone.now() - timezone.timedelta(days=7))
        for sheet_file in files:
            sheet_file.file.delete()
            sheet_file.delete()
            logger.info(f'Deleting sheet file {sheet_file.pk}')
