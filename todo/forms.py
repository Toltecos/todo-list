from django import forms

from todo.models import Task, Tag


class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "content": forms.Textarea(
                attrs={"placeholder": "Enter new task here", "rows": 5}
            ),
            "deadline_datetime": forms.DateTimeInput(
                attrs={"type": "datetime-local", "style": "width: 33%"}
            )
        }


class SearchForm(forms.Form):
    def __init__(self, search_field, search_query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[search_field] = forms.CharField(
            max_length=100,
            required=False,
            label="",
            initial=search_query,
            widget=forms.TextInput(
                attrs={
                    "placeholder": f"Search by {search_field}"
                }
            )
        )
