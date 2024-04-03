from django import forms
from .models import Reminder
from django.utils.translation import gettext_lazy as _

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'description', 'reminder_date', 'repetition_interval', 'urgency']
        
        
class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'description', 'reminder_date', 'repetition_interval', 'urgency']
        widgets = {
            'reminder_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'reminder_date': _('Reminder Date and Time'),
        }

