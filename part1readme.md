🚀 Secure File Sharing Application

==================📜 Overview====================
This application provides secure file sharing and management. Users can:

    Register
    Log in
    Upload files
    Download them securely
    Share files with others
    Files are encrypted to ensure privacy, and only authorized users can access them.

------------🛠️ Features:-----------------

🔐 User registration and login.
📤 File upload and download.
🔑 File sharing with encryption.
🛡️ Secure access control with user authentication.
⚙️ Admin panel for managing users and files.


---------------⚠️ Prerequisites:------------------
Before setting up the application, ensure you have the following:

Python 3.6 or higher 🐍
Django 5.1.3 (or higher) 🖥️
cryptography library for encryption 🔒
Install the dependencies:
Clone or download this repository.

########## Create a virtual environment and activate it: #################


        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate

##########Install Django and the cryptography library:####################

        pip install django cryptography

########Generate an encryption key using the cryptography package:##############

        python encryptionkey.py

        Save this key to an environment variable:
        we are using this key in the env file
                ''' Modification'''
        pip install python-dotenv ------ to read the env file for encryption key


----------🛠️ Setting Up the Application--------


->Create a new Django project using:


        django-admin startproject secure_file_sharing
        cd secure_file_sharing
        Step 2: Create the App

->Create the fileapp within your project:


        python manage.py startapp fileapp
        Step 3: Update settings.py



->Add fileapp to INSTALLED_APPS
In secure_file_sharing/settings.py, add the following settings:

        INSTALLED_APPS = [
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "fileapp",  # Our app <------------------------
            "django.contrib.staticfiles",
        ]
->Configure the encryption key by importing the key from the environment variable:

            import os
            from cryptography.fernet import Fernet

            ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY').encode()  # Use the environment variable
            fernet = Fernet(ENCRYPTI
            ON_KEY)  # Set up Fernet encryption
            Step 4: Configure URLs


->In secure_file_sharing/urls.py, add paths for your views:


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    ..........................
]


-> Create Models and Views
Define models and views in fileapp for file handling, user authentication, and encryption logic.

Views
Implement view functions such as upload_file, download_file, and share_file, handling file encryption and decryption.

-> Run Migrations
Create the database schema and apply migrations:

          ''' Modification'''
        python manage.py makemigrations fileapp
        python manage.py migrate
        
        

-> Create a Superuser
Create an admin user to manage the application:

        python manage.py createsuperuser

->Run the Application
Start the Django development server:

python manage.py runserver

->Test the Application
Visit http://127.0.0.1:8000/ to access the application.

Register a new user or log in using the superuser credentials.
Test uploading, downloading, and sharing encrypted files.
Access the admin panel at http://127.0.0.1:8000/admin/ to manage files and users.


Enjoy using the Secure File Sharing Application! 🔐🎉