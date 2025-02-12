"""
///////////////////////////////////////////////////////////////////////////
File Name: test_user_authentication.py
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
Test cases for user authentication, including registration, login, and form validation.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from fileapp.forms import RegistrationForm


class UserAuthenticationTests(TestCase):
    """
    Test cases for user registration, login, and validation of user input.
    """

    def setUp(self):
        """
        Set up the test client and create a sample user for authentication tests.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_registration_valid(self):
        """
        Test registering a new user with valid details.
        Expected Output:
            - Status code: 302 (redirect after successful registration).
            - New user is created in the database.
        """
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_duplicate_username(self):
        """
        Test registration with a username that already exists.
        Expected Output:
            - Error message indicating that the username is already taken.
        """
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'duplicate@example.com',
            'password': 'password123'
        })
        self.assertContains(response, 'This username is already taken.')

    def test_login_valid(self):
        """
        Test logging in with valid credentials.
        Expected Output:
            - Status code: 302 (redirect after successful login).
            - User is redirected to the file dashboard.
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('file_dashboard'))

    def test_login_invalid(self):
        """
        Test logging in with invalid credentials.
        Expected Output:
            - Error message indicating invalid username or password.
        """
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertContains(response, 'Invalid username or password')

    def test_login_form_instance(self):
        """
        Test that the login page renders correctly with the required fields.
        Expected Output:
            - Status code: 200 (successful page load).
            - Login form fields (username, password) are present in the response.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
