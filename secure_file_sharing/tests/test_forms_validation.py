"""
///////////////////////////////////////////////////////////////////////////
File Name: test_forms_validation.py
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
Test cases for validating user input in forms, particularly during registration.
"""

from django.test import TestCase
from django.urls import reverse
from fileapp.forms import RegistrationForm


class FormsValidationTests(TestCase):
    """
    Test cases to validate user input in registration forms, such as username,
    email, and password correctness.
    """

    def test_invalid_username_characters(self):
        """
        Test that the form rejects usernames with invalid characters.
        Expected Output:
            - The form is invalid.
            - Error message indicates invalid username characters.
        """
        form = RegistrationForm(data={
            'username': 'invalid!user',
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Username can only contain alphabetic characters and underscores.', form.errors['username'])

    def test_invalid_email(self):
        """
        Test that the form rejects invalid email addresses.
        Expected Output:
            - The form is invalid.
            - Error message indicates invalid email format.
        """
        form = RegistrationForm(data={
            'username': 'validuser',
            'email': 'invalid-email',
            'password': 'password123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', form.errors['email'])

    def test_empty_form_on_get_request(self):
        """
        Test that the registration page renders an empty form on a GET request.
        Expected Output:
            - Status code: 200 (successful page load).
            - The registration form fields are present in the response.
        """
        from django.test import Client
        client = Client()
        response = client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password"')
