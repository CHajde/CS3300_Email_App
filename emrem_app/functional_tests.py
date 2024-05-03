from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from emrem_app.models import Reminder
from django.utils import timezone

# Selenium testing --------------------------------------------

class UserRegistrationTest(StaticLiveServerTestCase):
    def setUp(self):
        # Setup code to open the web browser
        self.browser = webdriver.Chrome()

    def tearDown(self):
        # Cleanup code to close the web browser
        self.browser.quit()

    def test_user_registration_flow(self):
        # Directly navigate to the registration page
        self.browser.get(self.live_server_url + '/register/')  # Adjust the URL based on URLconf

        # Fill out the registration form
        self.browser.find_element(By.NAME, 'username').send_keys('newuser')
        self.browser.find_element(By.NAME, 'email').send_keys('user@example.com')
        self.browser.find_element(By.NAME, 'password1').send_keys('securepassword123')
        self.browser.find_element(By.NAME, 'password2').send_keys('securepassword123')

        # Submit the form
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        # Use WebDriverWait to wait for the redirect to complete
        WebDriverWait(self.browser, 10).until(
            EC.url_contains('login')  # Checks that 'login' is part of the current URL
        )


class UserLoginLogoutTest(StaticLiveServerTestCase):
    def setUp(self):
        # Setup code to open the web browser
        self.browser = webdriver.Chrome()
        User.objects.create_user('testuser', 'user@example.com', 'testpassword123')

    def tearDown(self):
        # Cleanup code to close the web browser
        self.browser.quit()

    def test_login_and_logout(self):
        # Navigate to the login page
        self.browser.get(self.live_server_url + '/login/')

        # Fill out the login form
        self.browser.find_element(By.NAME, 'username').send_keys('testuser')
        self.browser.find_element(By.NAME, 'password').send_keys('testpassword123')
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        # Verify redirect to home page or another protected page
        WebDriverWait(self.browser, 10).until(
            EC.url_contains('/')
        )

        # logout
        self.browser.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that user is redirected to login page
        WebDriverWait(self.browser, 10).until(
            EC.url_contains('login')
        )

        # Try to access a protected page
        self.browser.get(self.live_server_url + '/some_protected_page/')
        self.assertIn('login', self.browser.current_url)  # Checks if the 'login' is in the current URL


class ReminderCreationAndViewTest(StaticLiveServerTestCase):
    def setUp(self):
        # Setup code to open the web browser
        self.browser = webdriver.Chrome()
        User.objects.create_user('testuser', 'user@example.com', 'testpassword123')

    def tearDown(self):
        # Cleanup code to close the web browser
        self.browser.quit()

    def test_create_and_view_reminder(self):
        # Login first
        self.browser.get(self.live_server_url + '/login/')
        self.browser.find_element(By.NAME, 'username').send_keys('testuser')
        self.browser.find_element(By.NAME, 'password').send_keys('testpassword123')
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        # Navigate to the reminder creation page
        self.browser.get(self.live_server_url + '/create_reminder/')

        # Fill out the reminder form
        self.browser.find_element(By.NAME, 'title').send_keys('Test Reminder')
        self.browser.find_element(By.NAME, 'description').send_keys('This is a test reminder')
        self.browser.find_element(By.NAME, 'reminder_date').send_keys('2024-04-30 12:00')
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        # Now check if the reminder is listed on the reminders page
        self.browser.get(self.live_server_url + '/view_reminders/')
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Test Reminder', body_text)  # Check if the newly created reminder title is in the page content



class ReminderEditAndDeleteTest(StaticLiveServerTestCase):
    def setUp(self):
        # Setup code to open the web browser
        self.browser = webdriver.Chrome()
        user = User.objects.create_user('testuser', 'user@example.com', 'testpassword123')
        Reminder.objects.create(title='Initial Reminder', description='Initial Description', user=user, reminder_date=timezone.now())

    def tearDown(self):
        # Cleanup code to close the web browser
        self.browser.quit()

    def test_edit_and_delete_reminder(self):
        # Login first
        self.browser.get(self.live_server_url + '/login/')
        self.browser.find_element(By.NAME, 'username').send_keys('testuser')
        self.browser.find_element(By.NAME, 'password').send_keys('testpassword123')
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        # Navigate to the edit page of the reminder
        self.browser.get(self.live_server_url + '/edit_reminder/1/')

        # Change the title and description
        title_field = self.browser.find_element(By.NAME, 'title')
        title_field.clear()
        title_field.send_keys('Updated Reminder')
        description_field = self.browser.find_element(By.NAME, 'description')
        description_field.clear()
        description_field.send_keys('Updated Description')
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        # Verify changes
        self.browser.get(self.live_server_url + '/view_reminders/')
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Updated Reminder', body_text)
        self.assertIn('Updated Description', body_text)

        # Delete the reminder
        self.browser.find_element(By.LINK_TEXT, 'Delete').click()
        # Confirm the deletion
        self.browser.find_element(By.LINK_TEXT, 'Confirm Delete').click()

        # Verify the reminder is no longer listed
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Updated Reminder', body_text)
