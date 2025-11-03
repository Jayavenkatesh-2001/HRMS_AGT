from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from decimal import Decimal
from rms_app.models import Profile, Request

from rms_app.models import Request
from django.contrib import messages

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

from rms_app.models import Profile  # Ensure this exists




# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date  # ✅ Import system date
from rms_app.models import Profile
import re

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
import re

from rms_app.models import Profile  # Adjust if your Profile model is elsewhere

@login_required
def add_employee_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()  # ✅ Normalize email
        password = request.POST.get('password')
        role = request.POST.get('role')

        emp_id = request.POST.get('emp_id', '').strip()
        designation = request.POST.get('designation', '').strip()
        pan = request.POST.get('pan', '').strip()
        salary_lpa = request.POST.get('salary_lpa')

        # ✅ Full Name validation
        if not re.fullmatch(r'[A-Za-z ]+', username):
            messages.error(request, "Full Name must contain only alphabets and spaces.")
            return render(request, 'add_employee.html')

        # ✅ PAN validation
        if not re.fullmatch(r'[A-Z]{5}[0-9]{4}[A-Z]', pan):
            messages.error(request, "PAN must be 10 characters: 5 uppercase letters, 4 digits, and 1 uppercase letter.")
            return render(request, 'add_employee.html')

        # ✅ Email uniqueness check (case-insensitive)
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, f"Email '{email}' is already associated with another employee.")
            return render(request, 'add_employee.html')
        
        # ✅ PAN uniqueness check
        if Profile.objects.filter(pan=pan).exists():
            messages.error(request, f"PAN '{pan}' is already registered with another employee.")
            return render(request, 'add_employee.html')
        
        # ✅ Employee ID uniqueness check
        if Profile.objects.filter(emp_id=emp_id).exists():
            messages.error(request, f"Employee ID '{emp_id}' is already registered with another employee.")
            return render(request, 'add_employee.html')
        

        # ✅ Username uniqueness check
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' already exists.")
            return render(request, 'add_employee.html')

        # ✅ Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # ✅ Set role flags
        if role == 'admin':
            user.is_staff = True
        elif role == 'superuser':
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False

        user.save()

        # ✅ Create profile
        Profile.objects.create(
            user=user,
            role=role,
            emp_id=emp_id,
            designation=designation,
            pan=pan,
            salary_lpa=Decimal(salary_lpa) if salary_lpa else None,
            doj=date.today()
        )

        messages.success(request, f"Employee '{username}' added successfully.")
        return redirect('employee_credentials_superuser', user_id=user.id)

    return render(request, 'add_employee.html')



from django.http import JsonResponse
from django.contrib.auth.models import User

@login_required
def check_email_view(request):
    email = request.GET.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})


  # or wherever emp_id is stored

def check_emp_id(request):
    emp_id = request.GET.get('emp_id', '').strip()
    exists = Profile.objects.filter(emp_id=emp_id).exists()
    return JsonResponse({'exists': exists})




@login_required
def admin_dashboard(request):
    all_requests = Request.objects.all()
    return render(request, 'admin_dashboard.html', {'requests': all_requests})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rms_app.models import Request, Status
from django.utils import timezone



def home(request):
    recent_requests = Request.objects.order_by('-created_at')[:5]
    return render(request, 'home.html', {'requests': recent_requests})




from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


def employee_list(request):
    # Sort: users first, then admins
    users = User.objects.all().order_by('is_superuser', 'is_staff')
    return render(request, 'employee_list.html', {'users': users})







def edit_user_superuser(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        role = request.POST['role']

        user.save()

        if hasattr(user, 'profile'):
            user.profile.role = role
            user.profile.save()
        else:
            Profile.objects.create(user=user, role=role)

        return redirect('employee_list')

    return render(request, 'edit_user_superuser.html', {'user': user})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User


def employee_credentials_superuser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    context = {
        'user': user,
        'profile': profile
    }

    return render(request, 'employee_credentials_superuser.html', context)





def manage_employee_superuser(request):
    users = User.objects.all().order_by('is_superuser', 'is_staff')
    return render(request, 'manage_employee_superuser.html', {'users': users})


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User

def delete_user_superuser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_employee_superuser')


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('emp_list1')


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()

    # Redirect based on current user's role
    if request.user.is_superuser:
        return redirect('manage_employee_superuser')
    else:
        return redirect('manage_employee')  # for regular admins or staff
  # or wherever your list view is

def search(request):
    query = request.GET.get('q')
    results = User.objects.filter(username__icontains=query) if query else []
    return render(request, 'search.html', {'results': results, 'query': query})




@login_required
def search_role(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        current_user = request.user.username

        # Filter results based on the logged-in user's identity
        if current_user == 'admin':
            results = User.objects.filter(username__icontains=query, username='admin')
        elif current_user == 'superuser':
            results = User.objects.filter(username__icontains=query, username='superuser')
        elif current_user == 'user':
            results = User.objects.filter(username__icontains=query, username='user')

    return render(request, 'search_role.html', {
        'query': query,
        'results': results
    })
    


def view_user_superuser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    context = {
        'user': user,
        'profile': profile
    }

    return render(request, 'view_user_superuser.html', context)
