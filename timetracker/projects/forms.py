from django import forms

from timetracker.projects.models import Project


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Take sheet as an additional keyword argument.
        self.sheet = kwargs.pop('sheet')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        activity = super().save(commit=False)
        if self.sheet is not None:
            activity.sheet = self.sheet
        if commit:
            activity.save()
        return activity

    class Meta:
        model = Project
        fields = ('name', )
