from django import forms
from django.utils.translation import ugettext_lazy as _

from timetracker.activities.models import Activity
from timetracker.utils.widgets import DatePickerWidget, DateTimePickerWidget


class ActivityForm(forms.ModelForm):
    """
    Validate if activity is valid.
    """

    def __init__(self, *args, **kwargs):
        # Take sheet as an additional keyword argument to set it if
        # needed.
        self.sheet = kwargs.pop('sheet')
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = (
            self.fields['project'].queryset.filter(sheet_id=self.sheet.pk))

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
