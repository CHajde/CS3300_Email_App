from django.test import TestCase
from selenium import webdriver

# Create your tests here.
driver = webdriver.Chrome()
driver.get("http://www.google.com")
print(driver.title)  # Prints the title of the webpage opened
driver.quit()

