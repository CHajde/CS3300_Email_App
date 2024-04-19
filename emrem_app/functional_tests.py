from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UserRegistrationTest(StaticLiveServerTestCase):
    def setUp(self):
        # Setup code to open the web browser
        self.browser = webdriver.Chrome()

    def tearDown(self):
        # Cleanup code to close the web browser
        self.browser.quit()

    def test_user_registration_flow(self):
        # Directly navigate to the registration page
        self.browser.get(self.live_server_url + '/register/')  # Adjust the URL based on your URLconf

        # Fill out the registration form
        self.browser.find_element(By.NAME, 'username').send_keys('newuser')
        self.browser.find_element(By.NAME, 'email').send_keys('user@example.com')
        self.browser.find_element(By.NAME, 'password1').send_keys('securepassword123')
        self.browser.find_element(By.NAME, 'password2').send_keys('securepassword123')

        # Submit the form
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        # Use WebDriverWait to wait for the redirect to complete
        WebDriverWait(self.browser, 10).until(
            EC.url_contains('login')  # This checks that 'login' is part of the current URL
        )

