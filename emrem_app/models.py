from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.

class Reminder(models.Model):
    class Urgency(models.TextChoices):
        NOT_URGENT = 'NU', _('Not Urgent')
        SLIGHTLY_URGENT = 'SU', _('Slightly Urgent')
        VERY_URGENT = 'VU', _('Very Urgent')

    class RepetitionInterval(models.TextChoices):
        NONE = 'NO', _('No Repeat')
        FIVE_MIN_LATER = 'F5', _('Again 5 Minutes Later')
        TWO_TIMES_EVERY_FIVE = 'T25', _('Two Times Every 5 Minutes After First Reminder')
        THREE_TIMES_EVERY_FIVE = 'T35', _('Three Times Every 5 Minutes After First Reminder')

    title = models.CharField(max_length=200)
    description = models.TextField()
    reminder_date = models.DateTimeField()
    repetition_interval = models.CharField(
        max_length=3,
        choices=RepetitionInterval.choices,
        default=RepetitionInterval.NONE,
    )
    urgency = models.CharField(
        max_length=2,
        choices=Urgency.choices,
        default=Urgency.NOT_URGENT,
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('reminder-detail', args=[str(self.id)])
    
