from django import forms

from .models import Client


class AddEntryForm(forms.Form):

    client = forms.ModelChoiceField(queryset=Client.objects.all())

    class Meta:
        fields = ['client']
