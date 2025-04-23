from django.contrib import admin
from .models import EncryptedFile

@admin.register(EncryptedFile)
class EncryptedFileAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the EncryptedFile model.
    """
    list_display = ('user', 'file_name', 'sha256_hash')  # Show these fields in the list view
    filter_horizontal = ('shared_with',)  # Use a horizontal filter for the many-to-many 'shared_with' field
    search_fields = ('file_name', 'user__username')  # Allow search by file name or username
    list_filter = ('uploaded_at', 'file_type')       # Add filters by upload date or file type
    readonly_fields = ('sha256_hash', 'file_size', 'uploaded_at')  # Prevent edits to these fields