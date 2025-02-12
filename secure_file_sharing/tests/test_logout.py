"""
///////////////////////////////////////////////////////////////////////////
File Name: test_logout.py
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
Test cases for the logout functionality in the secure file-sharing application.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class LogoutViewTest(TestCase):
    """
    Test cases to validate logout behavior, including redirection and session invalidation.
    """

    def setUp(self):
        """
        Initialize the test client and log in a sample user.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_logout_redirects_to_home(self):
        """
        Test that logging out redirects the user to the home page.
        Expected Output:
            - Status code: 302 (redirect).
            - User is redirected to the home page URL.
        """
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))

    def test_user_logged_out(self):
        """
        Test that the user session is invalidated after logging out.
        Expected Output:
            - The username is no longer displayed on the home page.
        """
        self.client.get(reverse('logout'))  # Log the user out
        response = self.client.get(reverse('home'))  # Access the home page
        self.assertNotContains(response, 'testuser')  # Ensure the username is not displayed
