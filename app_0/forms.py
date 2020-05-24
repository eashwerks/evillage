from django import forms
from django.forms import TextInput

from app_0.models import RequestUser, RationCardService


class AbstractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            if self.fields[field].widget.__class__.__name__ in (
                    'TextInput', 'EmailInput', 'NumberInput', 'Select'):
                self.fields[field].widget.attrs.update({'class': 'form-control display-7'})


class RequestUserForm(AbstractForm):
    class Meta:
        model = RequestUser
        exclude = ('id',)


class RationCardServiceForm(AbstractForm):
    class Meta:
        model = RationCardService
        exclude = ('id',)
