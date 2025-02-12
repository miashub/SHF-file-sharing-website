"""
/////////////////////////////////////////////////////////////////////////// 
File Name:  views.py
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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from .forms import RegistrationForm, LoginForm
from .models import EncryptedFile
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings
import hashlib
import os

''' MODIFIED '''
# Access values from settings
ENCRYPTION_KEY = settings.ENCRYPTION_KEY
MAX_FILE_SIZE = settings.MAX_FILE_SIZE


cipher = Fernet(ENCRYPTION_KEY)  # Initialize the encryption cipher with the key


# Home view: Render the home page
def home_view(request):
    return render(request, 'home.html')  # Renders home page


# Registration View: Handle user registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)  # Instantiate form with POST data
        if form.is_valid():  # If the form is valid
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Create a new user and save it
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registration successful! You can now log in.')  # Success message
            return redirect('login')  # Redirect to login page
    else:
        form = RegistrationForm()  # Empty form for GET request
    return render(request, 'register.html', {'form': form})  # Render registration page with form


# Login View: Handle user login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Instantiate form with POST data
        if form.is_valid():  # If the form is valid
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # Authenticate the user
            if user:
                login(request, user)  # Log the user in
                return redirect('file_dashboard')  # Redirect to file dashboard page
            else:
                form.add_error(None, 'Invalid username or password')  # Add error if authentication fails
    else:
        form = LoginForm()  # Empty form for GET request
    return render(request, 'login.html', {'form': form})  # Render login page with form


# File Dashboard View: Display files uploaded and shared
@login_required  # Ensure the user is logged in
def file_dashboard(request):
    # Get files uploaded by the user and files shared with them
    uploaded_files = EncryptedFile.objects.filter(user=request.user)
    files_shared_with_me = EncryptedFile.objects.filter(shared_with=request.user)
    shared_files = EncryptedFile.objects.filter(user=request.user, shared_with__isnull=False).distinct()
    return render(request, 'file_dashboard.html', {
        'uploaded_files': uploaded_files,
        'files_shared_with_me': files_shared_with_me,
        'shared_files': shared_files
    })


# Handle file upload, encryption, and hash generation
@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):  # Check if a file is uploaded
        uploaded_file = request.FILES['file']
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'txt', 'mp3', 'mp4', 'zip', 'ppt']
        file_extension = uploaded_file.name.split('.')[-1].lower()  # Get file extension

        if file_extension not in allowed_extensions:
            messages.error(request, "Invalid file type!")  # Show error if the file type is not allowed
            return render(request, 'upload.html')  # Render the upload page again with the error message
        ''' MODIFIED '''
        #Check if the file exceeds the limit
        if uploaded_file.size > MAX_FILE_SIZE:
            messages.error(request, f"File size exceeds {settings.MAX_FILE_SIZE_MB} MB.")
            return redirect('upload')
        try:
            encrypted_content = cipher.encrypt(uploaded_file.read())
            hash_value = hashlib.sha256(encrypted_content).hexdigest()
            # Save the encrypted file and its hash in the database
            EncryptedFile.objects.create(
                user=request.user,
                file_name=uploaded_file.name,
                file_content=encrypted_content,
                sha256_hash=hash_value,
            )
            messages.success(request, 'File uploaded and encrypted successfully!')
        except Exception as e:
            messages.error(request, f"File upload failed: {e}")  # Show error if upload or encryption fails

        return render(request, 'upload.html')

    return render(request, 'upload.html')  # Render the upload form if GET request


# Download File View: Handle file decryption and download
@login_required  # Ensure the user is logged in
def download_file(request, file_id):
    # Check if the file exists and belongs to the user or is shared with them
    file = get_object_or_404(EncryptedFile, id=file_id)
    if file.user != request.user and request.user not in file.shared_with.all():
        messages.error(request, "You do not have permission to download this file.")  # Show error if no permission
        return redirect('file_dashboard')  # Redirect to file dashboard

    try:
        decrypted_content = cipher.decrypt(file.file_content)  # Decrypt the file content
        response = HttpResponse(decrypted_content, content_type='application/octet-stream')  # Return the decrypted content
        response['Content-Disposition'] = f'attachment; filename="{file.file_name}"'  # Suggest a filename for download
        return response
    except Exception as e:
        raise Http404(f"Error decrypting the file: {e}")  # Raise error if decryption fails


# Share File View: Share files with other users
@login_required  # Ensure the user is logged in
def share_file(request, file_id):
    file = get_object_or_404(EncryptedFile, id=file_id, user=request.user)  # Get the file owned by the current user
    if request.method == 'POST':
        usernames = request.POST.getlist('shared_users')  # Get list of usernames from the POST request
        ''' MODIFIED '''
        if not usernames:
            messages.warning(request, 'Please select at least one user to share the file with')  # Warning if no users are selected
            return redirect('share', file_id=file.id)  # Redirect back to the share page with the message
        for username in usernames:
            try:
                user = User.objects.get(username=username)  # Try to find the user by username
                file.shared_with.add(user)  # Add the user to the shared_with field
            except User.DoesNotExist:
                messages.warning(request, f"User '{username}' does not exist.")  # Warn if user does not exist
        file.save()  # Save the changes to the file object
        messages.success(request, 'File shared successfully!')  # Show success message
        return redirect('file_dashboard')  # Redirect to file dashboard page
    users = User.objects.exclude(username=request.user.username)  # Get all users except the current user
    return render(request, 'share.html', {'file': file, 'users': users})  # Render share page


# Logout View: Log out the user
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to home page
