from .models import Request
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect, render
from .forms import SignInForm, RequestForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, login as auth_login
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .forms import SignInForm
from .models import Profile  # Ensure this exists



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

# views.py
def user_dashboard(request):
    requests = Request.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'requests': requests})


def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    requests = Request.objects.all().order_by('-id')
    return render(request, 'admin_dashboard.html', {'requests':requests})

from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from .models import Request  # adjust import if needed

def update_request_status(request):
    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action = request.POST.get('action')

        try:
            req = Request.objects.get(id=req_id)
            req.status = action
            req.save()

            # Send email notification to requester
            subject = f"Your request #{req.id} has been {action}"
            message = f"Hello {req.user.first_name},\n\nYour request titled '{req.title}' has been updated to '{action}'.\n\nThank you,\nAdmin Team"
            recipient = req.user.email

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient],
                fail_silently=False
            )

            return JsonResponse({'success': True})

        except Request.DoesNotExist:
            return JsonResponse({'error': 'Request not found'}, status=404)



from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import RequestForm
from .models import Request

def submit_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.user = request.user
            req.save()

            subject = "New Request Submitted"
            message = "New request submitted. Want to approve or reject?"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.ADMIN_EMAIL]
            send_mail(subject, message, from_email, recipient_list)

            return render(request, 'request_success.html', {'form': form})
        else:
            return render(request, 'submit_request.html', {'form': form})
    else:
        form = RequestForm()
        return render(request, 'submit_request.html', {'form': form})

def request_overview(request):
    if request.user.is_superuser:
        requests = Request.objects.all().order_by('-created_at')
    else:
        requests = Request.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'request_overview.html', {'requests': requests})

    
 
    
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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from .models import Profile

@login_required
def add_employee_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        emp_id = request.POST.get('emp_id')
        designation = request.POST.get('designation')
        pan = request.POST.get('pan')
        salary_lpa = request.POST.get('salary_lpa')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' already exists.")
            return render(request, 'add_employee.html')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Set role flags based on selected role
        if role == 'admin':
            user.is_staff = True
        elif role == 'superuser':
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False

        user.save()

        # Create profile with extended data
        Profile.objects.create(
            user=user,
            role=role,
            emp_id=emp_id,
            designation=designation,
            pan=pan,
            salary_lpa=Decimal(salary_lpa) if salary_lpa else None
        )

        messages.success(request, f"Employee '{username}' added successfully.")
        return redirect('employee_credentials_superuser', user_id=user.id)


    return render(request, 'add_employee.html')


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def employee_credentials_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'employee_credentials.html', {'user': user})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from rms_app.models import Profile  # Adjust if your Profile model is elsewhere

def edit_user_detail(request, user_id):
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

        return redirect('emp_list1')

    return render(request, 'edit_user.html', {'user': user})

def aptsol_global_view(request):
    return render(request, 'aptsol_global.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Request  # Replace with your actual model name

@login_required
def user_dashboard(request):
    user_requests = Request.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {
        'requests': user_requests
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Request, Status
from django.utils import timezone

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Request
from .forms import RequestForm

@login_required
def submit_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.user = request.user
            req.save()
            messages.success(request, "Request submitted successfully.")
            return redirect('user_dashboard')
    else:
        form = RequestForm()
    return render(request, 'submit_request.html', {'form': form})


@login_required
def user_dashboard(request):
    user_requests = Request.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'requests': user_requests})

@login_required
def admin_dashboard(request):
    all_requests = Request.objects.all()
    return render(request, 'admin_dashboard.html', {'requests': all_requests})

def home(request):
    recent_requests = Request.objects.order_by('-created_at')[:5]
    return render(request, 'home.html', {'requests': recent_requests})

@login_required
def manage_requests(request):
    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action = request.POST.get('action_type')
        comment = request.POST.get('status_comment', '')

        req = get_object_or_404(Request, id=req_id)

        if action == 'approve':
            req.status = Status.APPROVED
        elif action == 'reject':
            req.status = Status.REJECTED

        req.status_comment = comment
        req.updated_by = request.user
        req.save()

        messages.success(request, f"Request {action}ed successfully.")
        return redirect('manage_requests')

    all_requests = Request.objects.all()
    return render(request, 'manage_requests.html', {'request': all_requests})





from django.shortcuts import render
from django.contrib.auth.models import User

def emp_list1_view(request):
    users = User.objects.filter(profile__role='user')
    return render(request, 'emp_list1.html', {'users': users})


from django.shortcuts import render
from django.contrib.auth.models import User

def manage_employee_view(request):
    users = User.objects.filter(profile__role='user')
    return render(request, 'manage_employee.html', {'users': users})



def change_password(request):
    return render(request, 'change_password.html')




def user_details(request):
    user = request.user
    # render user details
    return render(request, 'user_details.html', {'user': user})


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


def employee_list(request):
    # Sort: users first, then admins
    users = User.objects.all().order_by('is_superuser', 'is_staff')
    return render(request, 'employee_list.html', {'users': users})



@login_required
def manage_employees(request):
    return render(request, 'manage_employees.html')



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
from .models import Profile

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
    return redirect('manage_employee_superuser')  # or your desired redirect

    
    
    
    
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_employees')  # or whatever page you want to return to





def manage_employees(request):
    return render(request, 'manage_employee.html')





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
    

from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from num2words import num2words

def generate_payslip(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile

    now = datetime.now()
    current_year = now.year
    current_month_index = now.month

    
    selected_month = request.GET.get('month', now.strftime("%B %Y"))

    try:
        selected_month_name, selected_year = selected_month.split()
        selected_year = int(selected_year)
        selected_month_index = datetime.strptime(selected_month_name, "%B").month
    except ValueError:
        selected_month_index = None
        selected_year = None

    
    show_payslip = False
    warning_message = None

    if selected_year == current_year:
        if selected_month_index < current_month_index:
            show_payslip = True
        elif selected_month_index == current_month_index and now.day >= 28:
            show_payslip = True
        else:
            warning_message = f"The selected month ({selected_month}) is not yet completed. Payslip will be available after month-end."
    else:
        warning_message = f"The selected month ({selected_month}) is not valid for this year."


    salary_lpa = float(profile.salary_lpa or 0)
    monthly_salary = (salary_lpa * 100000) / 12
    basic = round(monthly_salary * 0.50, 2)
    hra = round(monthly_salary * 0.20, 2)
    special_allowance = round(monthly_salary * 0.20, 2)
    travel = 1260.00
    medical = 1260.00
    gross_earnings = round(basic + hra + special_allowance + travel + medical, 2)
    deductions = 800.00
    net_pay = round(gross_earnings - deductions, 2)
    net_words = num2words(net_pay, to='currency', lang='en_IN').replace('euro', 'rupees')

    # Month list
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    month_list = [f"{m} {current_year}" for m in month_names]

    context = {
        'user': user,
        'selected_month': selected_month,
        'month_list': month_list,
        'show_payslip': show_payslip,
        'warning_message': warning_message,
        'basic': basic,
        'hra': hra,
        'special_allowance': special_allowance,
        'travel': travel,
        'medical': medical,
        'gross_earnings': gross_earnings,
        'deductions': deductions,
        'net_pay': net_pay,
        'net_words': net_words,
    }

    return render(request, 'generate_payslip.html', context)




def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    context = {
        'user': user,
        'profile': profile
    }

    return render(request, 'view_user.html', context)

def view_user_superuser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    context = {
        'user': user,
        'profile': profile
    }

    return render(request, 'view_user_superuser.html', context)


from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from rms_app.models import Request
  # Replace with your actual model name

def update_request_status(request):
    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action = request.POST.get('action_type')

        req_obj = get_object_or_404(Request, id=req_id)

        if action == 'approve':
            req_obj.status = 'Approved'
            subject = 'Your request has been approved'
            message = f"Hi {req_obj.user.username},\n\nYour request for '{req_obj.requirement}' on {req_obj.date} has been approved."
        elif action == 'reject':
            req_obj.status = 'Rejected'
            subject = 'Your request has been rejected'
            message = f"Hi {req_obj.user.username},\n\nYour request for '{req_obj.requirement}' on {req_obj.date} has been rejected."
        else:
            messages.error(request, "Invalid action.")
            return redirect('manage_requests')

        req_obj.save()

        # Send email
        send_mail(
            subject,
            message,
             "jayavenkatesh.chukka2001@gmail.com",  # Replace with your sender email
            [req_obj.email],
            fail_silently=False,
        )

        messages.success(request, f"Request {action}ed and email sent.")
        return redirect('manage_requests')



def view_user_details(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    context = {
        'user': user,
        'profile': profile
    }

    return render(request, 'view_user_details.html', context)

