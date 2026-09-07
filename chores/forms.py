from django import forms

from .models import Chore


class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ["title", "description", "due_date"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }


class ChoreClaimForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=100)


class ChoreCompletionForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=100)
