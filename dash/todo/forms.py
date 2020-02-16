from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type = 'date'

class TodoForm(forms.Form):
    text = forms.CharField(max_length=40, widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter todo e.g. Delete junk files',
                   'aria-label': 'Todo',
                   'aria-describedby': 'add-btn'}))
    date = forms.DateField(widget=DateInput)