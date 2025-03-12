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

    def clean_tags(self):
        tags = self.cleaned_data.get("tags", [])
        existing_tags = Tag.objects.filter(id__in=[tag.id for tag in tags])
        return existing_tags


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name", "color"]
