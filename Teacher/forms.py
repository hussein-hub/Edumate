from django.forms import ModelForm, DateInput
from .models import Schedule

class EventForm(ModelForm):
  class Meta:
    model = Schedule
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'event_date': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = ['event_data','event_date']

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['event_date'].input_formats = ('%Y-%m-%dT%H:%M',)