"""
///////////////////////////////////////////////////////////////////////////
File Name: test_security.py
Group Number: 14
Group Members Names: Arushi Gopinath, Mia Shajahan
Group Members Seneca Email: fshajhan2@myseneca.ca agopinath@myseneca.ca
Date: 2024-12-07
Authenticity Declaration:
I declare this submission is the result of our group work and has not been
shared with any other groups/students or 3rd party content provider. This submitted
piece of work is entirely of my own creation.
//////////////////////////////
"""

"""
Test cases for security measures in the application, including resistance to SQL injection, 
Cross-Site Scripting (XSS), and secure handling of user inputs.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from fileapp.models import EncryptedFile
from cryptography.fernet import Fernet
from django.urls import reverse
from django.conf import settings

cipher = Fernet(settings.ENCRYPTION_KEY)

class SecurityTests(TestCase):
    """
    Test cases to ensure the application is secure from common vulnerabilities.
    """
    def setUp(self):
        """
        Set up the test client and create a sample user for security testing.
        """
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

    def test_sql_injection_resistance(self):
        """
        Test that the login form is resistant to SQL injection attacks.
        Expected Output:
            - Error message: 'Invalid username or password'.
            - No user is logged in with malicious input.
        """
        response = self.client.post(reverse('login'), {
            'username': "' OR '1'='1",
            'password': 'irrelevant'
        })
        self.assertContains(response, 'Invalid username or password')

    def test_xss_resistance_in_filenames(self):
        """
        Test that malicious filenames do not cause XSS vulnerabilities.
        Expected Output:
            - Malicious content is not executed or rendered in the response.
            - The filename is safely escaped in templates.
        """
        self.client.login(username='testuser', password='password123')
        malicious_filename = "<script>alert('XSS')</script>"
        file_content = cipher.encrypt(b'Sample content')
        EncryptedFile.objects.create(
            user=self.user,
            file_name=malicious_filename,
            file_content=file_content
        )
         # Ensure malicious script is not present in the response
        response = self.client.get(reverse('file_dashboard'))
        self.assertNotIn(malicious_filename, response.content.decode('utf-8'))

    def test_xss_injection_in_shared_files(self):
        """
        Test that XSS injections in the file-sharing functionality are mitigated.
        Expected Output:
            - Malicious content is not executed or rendered in the response.
            - Inputs are sanitized before being displayed.
        """
        file = EncryptedFile.objects.create(
            user=self.user,
            file_name="testfile.txt",
            file_content=cipher.encrypt(b"Sample content")
        )
        response = self.client.post(reverse('share', args=[file.id]), {
            'shared_users': ["<script>alert('XSS')</script>"]
        })
        self.assertNotIn("<script>", response.content.decode('utf-8'))
