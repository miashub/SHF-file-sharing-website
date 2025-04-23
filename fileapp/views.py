from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from .forms import RegistrationForm, LoginForm
from .models import EncryptedFile
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import hashlib, os, csv, mimetypes

# Initialize the cipher with the encryption key from settings
ENCRYPTION_KEY = settings.ENCRYPTION_KEY
MAX_FILE_SIZE = settings.MAX_FILE_SIZE
cipher = Fernet(ENCRYPTION_KEY)

def home_view(request):
    """Render the homepage view."""
    return render(request, 'home.html')


def register(request):
    """
    Handle user registration.
    If valid, creates a user and logs them in.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('file_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def check_username(request):
    """
    AJAX view to check username availability during registration.
    Returns JSON indicating availability.
    """
    username = request.GET.get('username')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'available': not exists})


def login_view(request):
    """
    Handle user login.
    Authenticate and log in the user if credentials are valid.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('file_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def file_dashboard(request):
    """
    Render the file dashboard showing uploaded files,
    files shared with the user, and files the user has shared.
    Includes filtering and searching functionality.
    """
    q = request.GET.get('q', '')
    filter_type = request.GET.get('filter', '')
    uploaded_files = EncryptedFile.objects.filter(user=request.user)

    if q:
        uploaded_files = uploaded_files.filter(file_name__icontains=q)
    if filter_type:
        if filter_type == 'pdf':
            uploaded_files = uploaded_files.filter(file_type='application/pdf')
        elif filter_type == 'text':
            uploaded_files = uploaded_files.filter(file_type__icontains='text')
        else:
            uploaded_files = uploaded_files.filter(file_type__icontains=filter_type)

    files_shared_with_me = EncryptedFile.objects.filter(shared_with=request.user)
    shared_files = EncryptedFile.objects.filter(user=request.user, shared_with__isnull=False).distinct()

    return render(request, 'file_dashboard.html', {
        'uploaded_files': uploaded_files,
        'files_shared_with_me': files_shared_with_me,
        'shared_files': shared_files,
        'query': q,
        'filter_type': filter_type,
    })


@login_required
def preview_file(request, file_id):
    """
    Allow previewing of image, text, pdf, or video files.
    Decrypts the content and returns a response with appropriate MIME type.
    """
    file = get_object_or_404(EncryptedFile, id=file_id)
    if file.user != request.user and request.user not in file.shared_with.all():
        return HttpResponse("Unauthorized", status=401)

    try:
        decrypted = cipher.decrypt(file.file_content)
        content_type = file.file_type or mimetypes.guess_type(file.file_name)[0] or 'application/octet-stream'

        if content_type.startswith(('image', 'video', 'text')) or content_type == 'application/pdf':
            return HttpResponse(decrypted, content_type=content_type)

        return HttpResponse("Preview not supported.", status=400)
    except Exception as e:
        return HttpResponse(f"Unable to preview this file. Error: {str(e)}", status=500)


@login_required
def delete_file(request, file_id):
    """
    Allow users to delete their own uploaded files.
    """
    file = get_object_or_404(EncryptedFile, id=file_id, user=request.user)
    file.delete()
    messages.success(request, "File deleted successfully.")
    return redirect('file_dashboard')


@login_required
def upload_file(request):
    """
    Handle file upload, validate type and size, encrypt content, and store metadata.
    """
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        custom_name = request.POST.get('custom_name', '').strip()

        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'txt', 'mp3', 'mp4', 'zip', 'pptx']
        file_extension = uploaded_file.name.split('.')[-1].lower()

        if file_extension not in allowed_extensions:
            messages.error(request, "Invalid file type!")
            return render(request, 'upload.html', {'MAX_FILE_SIZE_MB': settings.MAX_FILE_SIZE_MB})

        if uploaded_file.size > MAX_FILE_SIZE:
            messages.error(request, f"File size exceeds {settings.MAX_FILE_SIZE_MB} MB.")
            return render(request, 'upload.html', {'MAX_FILE_SIZE_MB': settings.MAX_FILE_SIZE_MB})

        try:
            encrypted_content = cipher.encrypt(uploaded_file.read())
            hash_value = hashlib.sha256(encrypted_content).hexdigest()
            file_size = uploaded_file.size
            mime_type, _ = mimetypes.guess_type(uploaded_file.name)
            final_name = custom_name or uploaded_file.name

            EncryptedFile.objects.create(
                user=request.user,
                file_name=final_name,
                file_content=encrypted_content,
                sha256_hash=hash_value,
                file_size=file_size,
                file_type=mime_type or ''
            )
            messages.success(request, 'File uploaded and encrypted successfully!')
        except Exception as e:
            messages.error(request, f"File upload failed: {e}")

        return render(request, 'upload.html', {'MAX_FILE_SIZE_MB': settings.MAX_FILE_SIZE_MB})

    return render(request, 'upload.html', {'MAX_FILE_SIZE_MB': settings.MAX_FILE_SIZE_MB})


@login_required
def download_file(request, file_id):
    """
    Allow authorized users to download a file.
    Decrypts content before sending the response.
    """
    file = get_object_or_404(EncryptedFile, id=file_id)
    if file.user != request.user and request.user not in file.shared_with.all():
        messages.error(request, "You do not have permission to download this file.")
        return redirect('file_dashboard')

    try:
        decrypted_content = cipher.decrypt(file.file_content)
        response = HttpResponse(decrypted_content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file.file_name}"'
        return response
    except Exception as e:
        raise Http404(f"Error decrypting the file: {e}")


@login_required
def share_file(request, file_id):
    """
    Allow a user to share a file they own with other registered users.
    """
    file = get_object_or_404(EncryptedFile, id=file_id, user=request.user)
    if request.method == 'POST':
        usernames = request.POST.getlist('shared_users')
        if not usernames:
            messages.warning(request, 'Please select at least one user to share the file with')
            return redirect('share', file_id=file.id)

        for username in usernames:
            try:
                user = User.objects.get(username=username)
                file.shared_with.add(user)
            except User.DoesNotExist:
                messages.warning(request, f"User '{username}' does not exist.")
        file.save()
        messages.success(request, 'File shared successfully!')
        return redirect('file_dashboard')

    users = User.objects.exclude(username=request.user.username)
    return render(request, 'share.html', {'file': file, 'users': users})


@login_required
def share_multiple_files(request):
    """
    Allow a user to share multiple selected files with a specific user.
    """
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        file_ids = request.POST.getlist('files')

        recipient = get_object_or_404(User, username=recipient_username)
        files_to_share = EncryptedFile.objects.filter(id__in=file_ids, user=request.user)

        for file in files_to_share:
            file.shared_with.add(recipient)

        messages.success(request, f"Shared {len(files_to_share)} files with {recipient_username}")
        return redirect('file_dashboard')

    users = User.objects.exclude(id=request.user.id)
    uploaded_files = EncryptedFile.objects.filter(user=request.user)
    return render(request, 'share_multiple.html', {
        'users': users,
        'uploaded_files': uploaded_files,
    })


def logout_view(request):
    """
    Log out the current user and redirect to home.
    """
    logout(request)
    return redirect('home')
