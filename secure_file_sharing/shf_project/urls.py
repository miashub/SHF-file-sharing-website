from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from fileapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('register/', views.register, name='register'),
    path('check_username/', views.check_username, name='check_username'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('file-dashboard/', views.file_dashboard, name='file_dashboard'),
    path('upload/', views.upload_file, name='upload'),
    path('download/<int:file_id>/', views.download_file, name='download'),
    path('share/<int:file_id>/', views.share_file, name='share'),
    path('delete/<int:file_id>/', views.delete_file, name='delete'),
    path('preview/<int:file_id>/', views.preview_file, name='preview'),
    path('share-multiple/', views.share_multiple_files, name='share_multiple'),
]

