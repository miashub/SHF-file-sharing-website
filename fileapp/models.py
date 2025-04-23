from django.db import models
from django.contrib.auth.models import User
import hashlib

class EncryptedFile(models.Model):
    """
    Model representing an encrypted file uploaded by a user.
    Stores metadata including SHA-256 hash, file size, type, and sharing relationships.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The owner/uploader of the file

    file_name = models.CharField(max_length=255)
    # Original name of the uploaded file

    file_content = models.BinaryField()
    # The encrypted content of the file (as binary data)

    sha256_hash = models.CharField(max_length=64, blank=True)
    # A SHA-256 hash of the file content for integrity verification

    file_size = models.IntegerField(default=0)
    # Size of the file in bytes

    uploaded_at = models.DateTimeField(auto_now_add=True)
    # Timestamp when the file was uploaded

    file_type = models.CharField(max_length=100, blank=True)
    # Optional field to store the MIME type (e.g., 'application/pdf')

    shared_with = models.ManyToManyField(User, related_name='shared_files', blank=True)
    # Users this file is shared with; supports multiple recipients

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically compute the SHA-256 hash
        of the file content if not already provided.
        """
        if self.file_content and not self.sha256_hash:
            # Compute the SHA-256 hash of the file content
            self.sha256_hash = hashlib.sha256(self.file_content).hexdigest()
        super().save(*args, **kwargs)
