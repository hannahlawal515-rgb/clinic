from django import forms

from .models import QueueEntry


class QueueEntryForm(forms.ModelForm):
    class Meta:
        model = QueueEntry
        fields = ("name", "phone", "service")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Jordan Lee", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"placeholder": "Optional", "autocomplete": "tel", "inputmode": "tel"}),
            "service": forms.Select(),
        }