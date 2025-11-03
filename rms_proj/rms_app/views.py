from rms_app.models import Request
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect, render
from rms_app.forms import SignInForm, RequestForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, login as auth_login
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from rms_app.forms import SignInForm
from rms_app.models import Profile  # Ensure this exists



def Signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role'].lower()

            # Check for existing username or email
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('Signin')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect('Signin')

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)

            # Assign role-based privileges
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False

            user.is_active = True  # ✅ Allow immediate login for both roles
            user.save()

            # Create profile
            Profile.objects.create(user=user, role=role)

            # Send welcome email
            subject = "Welcome to RMS"
            message = f"Hello {username},\n\nThank you for registering as a {role.capitalize()}!\n\nRegards,\nRMS Team"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            messages.success(request, "Signup successful! You can now log in.")
            return redirect('login')  # ✅ Redirect to login page
    else:
        form = SignInForm()

    return render(request, 'Signin.html', {'form': form})




from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)

            # Superuser check
            if role == 'superuser' and user.is_superuser:
                return redirect('home')

            # Admin check (non-superuser but has admin role)
            elif role == 'admin' and hasattr(user, 'profile') and user.profile.role == 'admin':
                return redirect('admin_dashboard')

            # Regular user check
            elif role == 'user' and hasattr(user, 'profile') and user.profile.role == 'user':
                return redirect('user_dashboard')

            else:
                messages.error(request, "Role mismatch. Please check your login role.")
        else:
            messages.error(request, "Invalid credentials or inactive account.")

    return render(request, 'login.html')




# @login_required
# def admin_dashboard(request):
#     return render(request, 'admin_dashboard.html')










    
 
    
@login_required
def logout_view(request):
        logout(request)
        messages.info(request, "Logged out successfully!")
        return redirect('login')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


















 # or whatever your directory view is named



from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')  # Make sure 'login' is defined in your urls.py
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def aptsol_global_view(request):
    return render(request, 'aptsol_global.html')











  # or your desired redirect

    
    
    
    






