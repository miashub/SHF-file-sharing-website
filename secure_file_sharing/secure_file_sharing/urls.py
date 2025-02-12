"""
/////////////////////////////////////////////////////////////////////////// 
File Name:  urls.py
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

from django.contrib import admin
from django.urls import path
from fileapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('file-dashboard/', views.file_dashboard, name='file_dashboard'),
    path('upload/', views.upload_file, name='upload'),
    path('download/<int:file_id>/', views.download_file, name='download'),
    path('share/<int:file_id>/', views.share_file, name='share'),
]