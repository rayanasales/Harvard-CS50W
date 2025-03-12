from django import forms
from .models import Task, Tag

class TaskForm(forms.ModelForm):
    date_to_complete = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'date_to_complete', 'size', 'priority', 'status', 'tags']