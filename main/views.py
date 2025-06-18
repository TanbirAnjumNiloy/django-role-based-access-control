# main/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.http import HttpResponse
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from .models import UserProfile

# ----------- Admin Signup View -----------

def admin_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        phone    = request.POST.get('phone')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already taken!")

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = UserProfile.objects.create(
            user=user,
            role='admin',
            phone=phone,
            signup_time=timezone.now()
        )

        login(request, user)
        return redirect('admin_page')

    return render(request, 'signup.html')

# ----------- Universal Login View -----------

def universal_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                profile = UserProfile.objects.get(user=user)
                role = profile.role

                if role == 'admin':
                    return redirect('admin_page')
                elif role == 'manager':
                    return redirect('manager_page')
                elif role == 'staff':
                    return redirect('staff_page')
                elif role == 'viewer':
                    return redirect('viewer_page')
                else:
                    return HttpResponse("Unknown role!")
            except UserProfile.DoesNotExist:
                return HttpResponse("User profile not found.")
        else:
            return HttpResponse("Invalid credentials!")

    return render(request, 'login.html')

# ----------- Role-Based Dashboards -----------

def admin_dashboard(request):
    return render(request, 'admin/admin.html')

def manager_dashboard(request):
    return render(request, 'manager/manager.html')

def staff_dashboard(request):
    return render(request, 'staff/staff.html')

def viewer_dashboard(request):
    return render(request, 'viewer/viewer.html') 


# main/views.py



@login_required
def makerole(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        phone    = request.POST.get('phone')
        password = request.POST.get('password')
        role     = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists!")

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create profile with role
        UserProfile.objects.create(
            user=user,
            role=role,
            phone=phone,
            signup_time=timezone.now(),
            created_by=request.user  # logged-in admin
        )

        return HttpResponse(f"User '{username}' with role '{role}' created successfully!")

    return render(request, 'admin/makerole.html')

