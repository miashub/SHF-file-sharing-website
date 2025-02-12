"""
///////////////////////////////////////////////////////////////////////////
File Name: test_file_sharing.py
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
Test cases for file sharing functionality in the secure file-sharing application.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from fileapp.models import EncryptedFile
from cryptography.fernet import Fernet
from django.urls import reverse
from django.conf import settings

cipher = Fernet(settings.ENCRYPTION_KEY)


class FileSharingTests(TestCase):
    """
    Test cases to verify file sharing functionality, including sharing with valid users,
    handling of invalid inputs, and error scenarios.
    """

    def setUp(self):
        """
        Initialize the test client, users, and log in the test user.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_share_file_valid_user(self):
        """
        Test sharing a file with a valid user.
        Expected Output:
            - Status code: 302 (redirect after sharing).
            - The shared user is added to the file's shared_with list.
        """
        content = b'Sample content'
        encrypted_content = cipher.encrypt(content)
        file = EncryptedFile.objects.create(
            user=self.user,
            file_name='testfile.txt',
            file_content=encrypted_content
        )
        response = self.client.post(reverse('share', args=[file.id]), {
            'shared_users': ['otheruser']
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('file_dashboard'))
        file.refresh_from_db()
        self.assertIn(self.other_user, file.shared_with.all())

    def test_share_file_no_user_selected(self):
        """
        Test sharing a file without selecting any users.
        Expected Output:
            - Redirects back to the share page.
        """
        content = b'Sample content'
        encrypted_content = cipher.encrypt(content)
        file = EncryptedFile.objects.create(
            user=self.user,
            file_name='testfile.txt',
            file_content=encrypted_content
        )
        response = self.client.post(reverse('share', args=[file.id]), {
            'shared_users': []
        })
        self.assertRedirects(response, reverse('share', args=[file.id]))

    def test_share_file_invalid_user(self):
        """
        Test sharing a file with a non-existent user.
        Expected Output:
            - Status code: 302 (redirect after unsuccessful sharing).
        """
        content = b'Sample content'
        encrypted_content = cipher.encrypt(content)
        file = EncryptedFile.objects.create(
            user=self.user,
            file_name='testfile.txt',
            file_content=encrypted_content
        )
        response = self.client.post(reverse('share', args=[file.id]), {
            'shared_users': ['nonexistentuser']
        })
        self.assertRedirects(response, reverse('file_dashboard'))
