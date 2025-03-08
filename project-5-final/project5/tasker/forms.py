from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    date_to_complete = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Task
        fields = ["name", "description", "date_to_complete", "size", "priority", "status"]