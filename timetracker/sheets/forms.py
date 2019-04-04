from django import forms

from timetracker.sheets.models import TimeSheet


class TimeSheetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Take user as an additional keyword argument to set it if
        # needed.
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        sheet = super().save(commit=False)
        if self.user is not None:
            sheet.user = self.user
        if commit:
            sheet.save()
        return sheet

    class Meta:
        model = TimeSheet
        fields = ('title', )
