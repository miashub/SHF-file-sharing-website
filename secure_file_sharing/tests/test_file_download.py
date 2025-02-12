"""
///////////////////////////////////////////////////////////////////////////
File Name: test_file_download.py
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
Test cases for file download functionality in the secure file-sharing application.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from fileapp.models import EncryptedFile
from cryptography.fernet import Fernet
from django.urls import reverse
import hashlib
from django.conf import settings
from unittest.mock import patch

cipher = Fernet(settings.ENCRYPTION_KEY)


class FileDownloadTests(TestCase):
    """
    Test cases for validating file download functionality, including authorized downloads,
    unauthorized access, and error handling.
    """

    def setUp(self):
        """
        Initialize the test client and a sample user for the tests.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_file_download_own_file(self):
        """
        Test downloading a file owned by the user.
        Expected Output:
            - Status code: 200 (success)
            - Response content matches the original file's content after decryption.
        """
        content = b'Sample content'
        encrypted_content = cipher.encrypt(content)
        file = EncryptedFile.objects.create(
            user=self.user,
            file_name='testfile.txt',
            file_content=encrypted_content,
            sha256_hash=hashlib.sha256(encrypted_content).hexdigest()
        )
        response = self.client.get(reverse('download', args=[file.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, content)

    def test_file_download_unauthorized(self):
        """
        Test downloading a file owned by another user.
        Expected Output:
            - Status code: 302 (redirect, unauthorized access).
        """
        other_user = User.objects.create_user(username='otheruser', password='password123')
        content = b'Sample content'
        encrypted_content = cipher.encrypt(content)
        file = EncryptedFile.objects.create(
            user=other_user,
            file_name='testfile.txt',
            file_content=encrypted_content
        )
        response = self.client.get(reverse('download', args=[file.id]))
        self.assertEqual(response.status_code, 302)

    @patch('fileapp.views.cipher.decrypt')
    def test_file_download_decryption_error(self, mock_decrypt):
        """
        Test decryption failure during file download.
        Expected Output:
            - Status code: 404 (file not retrievable).
        """
        mock_decrypt.side_effect = Exception("Decryption failed")

        content = b'Sample content'
        encrypted_content = cipher.encrypt(content)
        file = EncryptedFile.objects.create(
            user=self.user,
            file_name='testfile.txt',
            file_content=encrypted_content,
            sha256_hash=hashlib.sha256(encrypted_content).hexdigest()
        )

        response = self.client.get(reverse('download', args=[file.id]))
        self.assertEqual(response.status_code, 404)
