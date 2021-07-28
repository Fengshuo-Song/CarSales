from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

# app_name = 'account'

urlpatterns = [
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls'), name = 'login'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]
