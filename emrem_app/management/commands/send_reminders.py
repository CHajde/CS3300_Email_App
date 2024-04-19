from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from emrem_app.models import Reminder
from django.conf import settings
import ssl

class Command(BaseCommand):
    help = 'Sends reminders that are due'

    # Monkey-patch SSL to ignore certificate verification | VERY BAD PRACTICE, NEVER USE IN PRODUCTION
    ssl._create_default_https_context = ssl._create_unverified_context
    
    
    def handle(self, *args, **options):
        current_time = timezone.localtime()  # Ensure time is timezone aware
        start_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = current_time.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Get reminders for today that haven't been sent yet
        reminders = Reminder.objects.filter(
            reminder_date__gte=start_of_day,
            reminder_date__lte=end_of_day,
            sent=False  # Ensure that the reminder has not been marked as sent
        )

        for reminder in reminders:
            subject = f"Reminder: {reminder.title}"
            if reminder.urgency == 'VU':
                subject = f"URGENT: {reminder.title}"
            elif reminder.urgency == 'SU':
                subject = f"Important: {reminder.title}"


            send_mail(
                subject,
                reminder.description,
                'PromptlyReminders@gmail.com',
                [reminder.user.email],
                fail_silently=False,
            )
            reminder.sent = True  # Mark the reminder as sent
            reminder.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully sent reminder {reminder.id}'))
