from django import forms
import datetime
from django.contrib import messages

from . import models

class DataInput(forms.DateInput):
    input_type = 'date'



class TodoForm(forms.Form):
    GROUP_CHOICES = (
        ('','Select Todo Type'),
        ('School', 'School'),
        ('Leisure', 'Leisure'),
        ('Financial', 'Financial'),
        ('Misc', 'Miscellaneous')
    )

    text = forms.CharField(max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Todo e.g. Delete junk files',
                   'aria-label': 'Todo',
                   'aria-describedby': 'add-btn'}))
    date = forms.DateField(widget=DataInput)
    group = forms.ChoiceField(label="category", widget=forms.Select, choices=GROUP_CHOICES)

    # def clean_date(self):
    #     date = self.cleaned_data['date']
    #     if date < datetime.date.today():
    #         raise forms.ValidationError("The date cannot be in the past!")
    #     return date
