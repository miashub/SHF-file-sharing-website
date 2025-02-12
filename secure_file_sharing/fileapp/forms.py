"""
/////////////////////////////////////////////////////////////////////////// 
File Name:  forms.py
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

from django import forms
from django.contrib.auth.models import User
import re

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Check if the username contains only alphabetic characters and underscores
        if not re.match(r'^[a-zA-Z_]+$', username):
            raise forms.ValidationError("Username can only contain alphabetic characters and underscores.")
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")

        return username

# Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
