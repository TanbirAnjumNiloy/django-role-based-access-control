# RBAC/urls.py

from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    # Signup and Login
    path('signup/', views.admin_signup, name='signup'),
    path('', views.universal_login, name='login'),

    # Dashboard for each role
    path('admin-dashboard/', views.admin_dashboard, name='admin_page'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_page'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_page'),
    path('viewer-dashboard/', views.viewer_dashboard, name='viewer_page'),

    path('makerole/', views.makerole, name='makerole'),


    
]
