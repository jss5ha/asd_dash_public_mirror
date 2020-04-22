from django.forms import ModelForm, DateInput
from .models import Event

#am i tracking right???

class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = ('title', 'start_time', 'end_time')
  def clean(self):
        super(EventForm, self).clean()
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')
     
        if end_time < start_time:
            self._errors['end_time'] = self.error_class(['The starting time must be before the ending time.'])

       
        return self.cleaned_data

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)