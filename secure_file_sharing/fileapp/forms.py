from django import forms
from django.contrib.auth.models import User
import re

class RegistrationForm(forms.Form):
    """
    Form for registering a new user.
    Includes fields for username, email, password, and password confirmation.
    Includes validation for unique username, valid characters, password length, and matching passwords.
    """
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean_username(self):
        """
        Validates the username to allow alphanumeric characters and underscores.
        Also checks that the username is not already taken.
        """
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError("Username can only contain letters, numbers, and underscores.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


    def clean_password(self):
        """
        Ensures the password is at least 8 characters long.
        """
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean(self):
        """
        Validates that the password and confirm password fields match.
        Adds an error to confirm_password if they do not match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            self.add_error("confirm_password", "Passwords do not match.")


class LoginForm(forms.Form):
    """
    Form for logging in a user.
    Requires username and password fields.
    """
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
