from django.contrib import admin
from .models import EncryptedFile

@admin.register(EncryptedFile)
class EncryptedFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_name', 'sha256_hash')  # Fields to show in the admin list
    filter_horizontal = ('shared_with',)  # For ManyToMany fields.
