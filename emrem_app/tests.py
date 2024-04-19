from django.test import TestCase
from django.urls import reverse
from .models import Reminder
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .forms import ReminderForm



class ReminderModelTests(TestCase):
    def setUp(self):
        # Create a user for the test cases
        self.user = User.objects.create_user(username='testuser', password='12345678')

    def test_create_reminder(self):
        reminder = Reminder.objects.create(
        user=self.user,
        title='Appointment',
        description='Dentist appointment.',
        reminder_date=timezone.make_aware(datetime.datetime(2023, 4, 30, 14, 30)),
        repetition_interval=Reminder.RepetitionInterval.NONE,
        urgency=Reminder.Urgency.NOT_URGENT
    )
        self.assertIsInstance(reminder, Reminder)

    def test_reminder_string_representation(self):
        # Test the string representation of a reminder
        reminder = Reminder(
            title='Appointment',
            description='Dentist appointment.',
            reminder_date='2023-04-30 14:30:00',
            repetition_interval=Reminder.RepetitionInterval.NONE,
            urgency=Reminder.Urgency.NOT_URGENT
        )
        self.assertEqual(str(reminder), 'Appointment')



class ReminderFormTests(TestCase):
    def setUp(self):
        # Create a user for the test cases
        self.user = User.objects.create_user(username='testuser', password='12345678')

    def test_form_validation_error(self):
        # Create form with missing required fields
        form_data = {
            'title': '',  # Required field left blank
            'description': 'Need to visit the dentist',
            'reminder_date': timezone.now(),
            'repetition_interval': Reminder.RepetitionInterval.NONE,
            'urgency': Reminder.Urgency.NOT_URGENT
        }
        form = ReminderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)  # Ensure 'title' field has errors

    def test_form_save(self):
        # Create form with all required fields
        form_data = {
            'title': 'Dentist Appointment',
            'description': 'Annual checkup',
            'reminder_date': timezone.now(),
            'repetition_interval': Reminder.RepetitionInterval.NONE,
            'urgency': Reminder.Urgency.NOT_URGENT
        }
        form = ReminderForm(data=form_data)
        self.assertTrue(form.is_valid())
        reminder = form.save(commit=False)
        reminder.user = self.user
        reminder.save()
        
        # Check that the reminder was added to the database
        self.assertEqual(Reminder.objects.count(), 1)
        self.assertEqual(Reminder.objects.first().title, 'Dentist Appointment')
        


class ReminderViewTests(TestCase):
    def setUp(self):
        # Create a user and log in
        self.user = User.objects.create_user(username='testuser', password='12345678')
        self.client.login(username='testuser', password='12345678')

        # Create a reminder for this user
        self.reminder = Reminder.objects.create(
            user=self.user,
            title="Doctor Appointment",
            description="Annual check-up",
            reminder_date=timezone.now(),
            repetition_interval=Reminder.RepetitionInterval.NONE,
            urgency=Reminder.Urgency.NOT_URGENT
        )

    def test_view_reminders_access_control(self):
        # Log out the user first to test access control
        self.client.logout()
        response = self.client.get(reverse('view_reminders'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('view_reminders')}")

    def test_create_reminder_view_with_valid_data(self):
        # Ensure authenticated user can post valid data
        form_data = {
            'title': 'New Appointment',
            'description': 'Meeting with client.',
            'reminder_date': timezone.now(),
            'repetition_interval': Reminder.RepetitionInterval.NONE,
            'urgency': Reminder.Urgency.NOT_URGENT
        }
        response = self.client.post(reverse('create_reminder'), form_data)
        self.assertEqual(response.status_code, 302)  # Check for redirect (successful creation)
        self.assertEqual(Reminder.objects.count(), 2)  # Check that a new reminder was added