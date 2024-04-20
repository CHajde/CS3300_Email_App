from django.core.management.base import BaseCommand
from django.utils import timezone
from emrem_app.models import Reminder
import smtplib
from email.message import EmailMessage
import ssl
import certifi

class Command(BaseCommand):
    help = 'Sends reminders that are due'

    def send_email(self, subject, body, to_email):
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = 'PromptlyReminders@gmail.com'
        msg['To'] = to_email

        ssl_context = ssl.create_default_context(cafile=certifi.where())
                
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls(context=ssl_context)
            server.ehlo()
            server.login('promtplyreminders@gmail.com', 'ximuaqnfthricuin')
            server.send_message(msg)

    def handle(self, *args, **options):
        current_time = timezone.localtime()  # Ensure time is timezone aware
        start_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = current_time.replace(hour=23, minute=59, second=59, microsecond=999999)

        reminders = Reminder.objects.filter(
            reminder_date__gte=start_of_day,
            reminder_date__lte=end_of_day,
            sent=False
        )

        for reminder in reminders:
            subject = f"Reminder: {reminder.title}"
            if reminder.urgency == 'VU':
                subject = f"URGENT: {reminder.title}"
            elif reminder.urgency == 'SU':
                subject = f"Important: {reminder.title}"

            self.send_email(
                subject,
                reminder.description,
                reminder.user.email
            )
            reminder.sent = True
            reminder.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully sent reminder {reminder.id}'))
