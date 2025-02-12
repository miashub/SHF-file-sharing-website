"""
/////////////////////////////////////////////////////////////////////////// 
File Name:  models.py
Group Number: 14
Group Members Names: Arushi Gopinath, Mia Shajahan
Group Members Seneca Email: fshajhan2@myseneca.ca agopinath@myseneca.ca
Date: 2024-11-21
Authenticity Declaration:
I declare this submission is the result of our group work and has not been
shared with any other groups/students or 3rd party content provider. This submitted
piece of work is entirely of my own creation.
/////////////////////////////////////////////////////////////////////////// 
"""


from django.db import models
from django.contrib.auth.models import User
import hashlib

# Model to store encrypted files, associated with a user
class EncryptedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who uploaded the file
    file_name = models.CharField(max_length=255)  # The name of the file
    file_content = models.BinaryField()  # Store the encrypted file content as binary data
    sha256_hash = models.CharField(max_length=64, blank=True)  # File integrity check using SHA-256 hash
    shared_with = models.ManyToManyField(User, related_name='shared_files', blank=True)  # Users who have access to the file

    def save(self, *args, **kwargs):
        # Generate file hash for integrity if the file content is present
        if self.file_content:
            self.sha256_hash = hashlib.sha256(self.file_content).hexdigest()  # Create SHA-256 hash of the file content
        super().save(*args, **kwargs)  # Call the parent class save method to store the file
