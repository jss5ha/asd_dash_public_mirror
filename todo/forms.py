from django import forms
import datetime
from django.contrib import messages

from . import models

class DataInput(forms.DateInput):
    input_type = 'date'

class TodoForm(forms.Form):
    text = forms.CharField(max_length=40, widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter todo e.g. Delete junk files',
                   'aria-label': 'Todo',
                   'aria-describedby': 'add-btn'}))
    date = forms.DateField(widget=DataInput)

    # def clean_date(self):
    #     date = self.cleaned_data['date']
    #     if date < datetime.date.today():
    #         raise forms.ValidationError("The date cannot be in the past!")
    #     return date
