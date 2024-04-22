from django.core.management.base import BaseCommand
from django.utils import timezone
from emrem_app.models import Reminder
import smtplib
from email.message import EmailMessage
import ssl
import certifi

class Command(BaseCommand):
    help = 'Sends reminders that are due'

    def send_email(self, subject, body, to_email, reminder_time, username, urgency_label):
        msg = EmailMessage()
        
        # Convert reminder_time to local timezone
        local_reminder_time = timezone.localtime(reminder_time)
        
        # Setting the subject to include reminder title and time
        msg['Subject'] = f"{subject} Today at {local_reminder_time.strftime('%H:%M')}"
        msg['From'] = 'PromptlyReminders@gmail.com'
        msg['To'] = to_email

        # Formatting the body of the email
        email_body = (f"Hello, {username}. You have a {urgency_label} reminder set for today.\n\n"
                  f"Description of your Reminder:\n{body}\n\n"
                  "This is an automated email, please do not respond.\n"
                  "Thank you for using Promptly!")
                     
        msg.set_content(email_body)

        # Use certifi to get the path to the CA bundle and create a SSL context
        ssl_context = ssl.create_default_context(cafile=certifi.where())
                
        # Send the email using Gmail's SMTP server and the provided credentials
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls(context=ssl_context)
            server.ehlo()
            server.login('promtplyreminders@gmail.com', 'ximuaqnfthricuin') # Unfortunate typo in the email address, cannot be fixed
            server.send_message(msg)

    def handle(self, *args, **options):
        current_time = timezone.localtime()  # Ensure time is timezone aware
        start_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = current_time.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        print(f"Current Time: {current_time}")
        print(f"Start of Day: {start_of_day}")
        print(f"End of Day: {end_of_day}")

        # Get reminders that are due today and have not been sent
        reminders = Reminder.objects.filter(
            reminder_date__gte=start_of_day,
            reminder_date__lte=end_of_day,
            sent=False
        )
        
        print(f"Found {reminders.count()} reminders due today.")

        if reminders.exists():
            for reminder in reminders:
                subject = f"Reminder: {reminder.title}"
                if reminder.urgency == 'VU':
                    subject = f"URGENT: {reminder.title}"
                elif reminder.urgency == 'SU':
                    subject = f"Important: {reminder.title}"

                # Call the send_email function which actually sends the email
                self.send_email(
                    subject,
                    reminder.description,
                    reminder.user.email,
                    reminder.reminder_date,
                    reminder.user.username,
                    reminder.get_urgency_display()
                )
                # Set the reminder as 'sent' so it is not sent again
                reminder.sent = True
                reminder.save()

                # Prints in the console that the reminder was sent, if successful
                self.stdout.write(self.style.SUCCESS(f'Successfully sent reminder {reminder.id}'))
        else:
            # Print a message when no reminders are due to be sent
            self.stdout.write(self.style.WARNING('No reminders are due to be sent at this time.'))
