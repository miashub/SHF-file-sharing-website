"""
///////////////////////////////////////////////////////////////////////////
File Name: test_file_upload.py
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
Test cases for file upload functionality in the secure file-sharing application.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from fileapp.models import EncryptedFile
from cryptography.fernet import Fernet
from django.urls import reverse
from django.conf import settings
from unittest.mock import patch
import os

cipher = Fernet(settings.ENCRYPTION_KEY)

class FileUploadTests(TestCase):
    """
    Test cases for file upload, including validation of file type, size, and encryption.
    """

    def setUp(self):
        """
        Set up the test client and create a sample user for uploading tests.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_invalid_file_extension(self):
        """
        Test that the system rejects files with invalid extensions.
        Expected Output:
            - Error message indicating invalid file type.
        """
        with open('testfile.exe', 'w') as f:
            f.write("Invalid content")
        with open('testfile.exe', 'rb') as f:
            response = self.client.post(reverse('upload'), {'file': f})
        os.remove('testfile.exe')
        self.assertContains(response, "Invalid file type!")

    def test_file_upload_valid(self):
        """
        Test uploading a valid file.
        Expected Output:
            - Success message indicating the file was uploaded and encrypted.
            - The file is added to the database.
        """
        with open('testfile.txt', 'w') as f:
            f.write("Sample content")
        with open('testfile.txt', 'rb') as f:
            response = self.client.post(reverse('upload'), {'file': f})
        os.remove('testfile.txt')
        self.assertContains(response, 'File uploaded and encrypted successfully!')
        self.assertEqual(EncryptedFile.objects.count(), 1)

    def test_file_size_limit(self):
        """
        Test that the system rejects files exceeding the size limit.
        Expected Output:
            - Status code: 302 (redirect due to size limit).
        """
        large_content = b'A' * (settings.MAX_FILE_SIZE + 1)
        with open('largefile.txt', 'wb') as f:
            f.write(large_content)

        with open('largefile.txt', 'rb') as f:
            response = self.client.post(reverse('upload'), {'file': f})

        os.remove('largefile.txt')
        self.assertEqual(response.status_code, 302)

    @patch('fileapp.views.cipher.encrypt')
    @patch('fileapp.models.EncryptedFile.objects.create')
    def test_file_upload_exception(self, mock_create, mock_encrypt):
        """
        Test handling encryption failure during file upload.
        Expected Output:
            - Error message indicating the upload failed due to encryption issues.
            - No files are added to the database.
        """
        mock_encrypt.side_effect = Exception("Encryption failed")

        with open('testfile.txt', 'w') as f:
            f.write("Sample content")
        with open('testfile.txt', 'rb') as f:
            response = self.client.post(reverse('upload'), {'file': f})
        os.remove('testfile.txt')

        self.assertContains(response, "File upload failed: Encryption failed")
        self.assertEqual(EncryptedFile.objects.count(), 0)

    def test_upload_page_renders_on_get(self):
        """
        Test that the upload page renders correctly on a GET request.
        Expected Output:
            - Status code: 200 (successful page load).
            - The upload form is present in the response.
        """
        response = self.client.get(reverse('upload'))
        self.assertTemplateUsed(response, 'upload.html')
        self.assertContains(response, 'enctype="multipart/form-data"')
