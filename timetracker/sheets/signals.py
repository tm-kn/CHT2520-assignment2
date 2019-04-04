import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from timetracker.sheets.models import TimeSheet

logger = logging.getLogger(__name__)


def create_timesheet_on_user_creation(instance, created, **kwargs):
    if not created:
        return

    TimeSheet.objects.create(title="Default", user=instance)
    logger.info("Created default timesheet for user %s (UID:%d)",
                instance.email, instance.pk)


def register_signals():
    post_save.connect(
        create_timesheet_on_user_creation,
        sender=get_user_model(),
        dispatch_uid='create_timesheet_on_user_creation')
