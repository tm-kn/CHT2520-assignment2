from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from timetracker.activities.models import Activity
from timetracker.utils.widgets import DatePickerWidget, DateTimePickerWidget


class ActivityForm(forms.ModelForm):
    """
    Validate if activity is valid.
    """

    def __init__(self, *args, **kwargs):
        # Sheet is required for the working of this form.
        self.sheet = kwargs.pop('sheet')
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = (
            self.fields['project'].queryset.filter(sheet_id=self.sheet.pk))

    def clean_start_datetime(self):
        value = self.cleaned_data['start_datetime']

        if value and value > timezone.now():
            raise forms.ValidationError(
                _('Cannot add activity that starts in the future.'))
        return value

    def clean_end_datetime(self):
        value = self.cleaned_data['end_datetime']

        if value and value > timezone.now():
            raise forms.ValidationError(
                _('Cannot add activity that ends in the future.'))
        return value

    def validate_start_time_is_smaller(self, start_time, end_time):
        """
        Validate end datetime is not before start datetime.
        """
        if end_time and start_time \
                and end_time <= start_time:
            raise forms.ValidationError({
                'start_datetime':
                [_('End datetime must be greater than the start datetime.')]
            })

    def check_for_overlaps(self, sheet, start_time, end_time):
        if start_time is None:
            return

        activities = sheet.activities.all()

        if self.instance.pk:
            activities = activities.exclude(pk=self.instance.pk)

        # Check if there's an active activity.
        try:
            active_activity = activities.get(end_datetime__isnull=True)
        except ObjectDoesNotExist:
            active_activity = None

        if active_activity:
            if end_time is None:
                raise forms.ValidationError({
                    'end_datetime': [
                        _('You need to stop current activity before you '
                          'add this one.'),
                    ]
                })
            if active_activity.start_datetime <= end_time:
                raise forms.ValidationError({
                    'start_datetime': [
                        _('Your activity overlaps with the current '
                          'activity.'),
                    ]
                })

        # If there's no errors regarding active activity, check for other
        # overlaps.
        overlap = activities.exclude(end_datetime__isnull=True).filter(
            start_datetime__lte=end_time or timezone.now(),
            end_datetime__gte=start_time)

        if overlap.exists():
            raise forms.ValidationError({
                'start_datetime':
                [_('Your activity overlaps with a different '
                   'activity.')]
            })

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_datetime')
        end_time = cleaned_data.get('end_datetime')
        sheet = self.sheet

        self.validate_start_time_is_smaller(start_time, end_time)
        self.check_for_overlaps(sheet, start_time, end_time)

    def save(self, commit=True):
        activity = super().save(commit=False)
        if self.sheet is not None:
            activity.sheet = self.sheet
        if commit:
            activity.save()
        return activity

    class Meta:
        model = Activity
        fields = (
            'project',
            'activity',
            'description',
            'start_datetime',
            'end_datetime',
        )
        # Use custom JS widgets for the datetime fields.
        widgets = {
            'start_datetime': DateTimePickerWidget(),
            'end_datetime': DateTimePickerWidget(),
        }


class ActivityFilterForm(forms.Form):
    """
    Validate activity filters.
    """
    start_date = forms.DateField(
        required=False, widget=DatePickerWidget(), label=_('Start date'))
    end_date = forms.DateField(
        required=False, widget=DatePickerWidget(), label=_('End date'))
    search_query = forms.CharField(required=False, label=_('Search query'))
