from django import forms

from timetracker.models import Client


class AddEntryForm(forms.Form):

    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False)
    url = forms.URLField()

    class Meta:
        fields = ['client', 'url']
