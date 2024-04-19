from django import forms
from .models import Reminder
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
        
        
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


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')