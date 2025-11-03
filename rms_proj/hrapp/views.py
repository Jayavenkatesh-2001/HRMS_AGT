from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from datetime import datetime
from num2words import num2words

from rms_app.models import Request, Status, Profile
from rms_app.forms import SignInForm, RequestForm

# Admin check
def is_admin(user):
    return user.is_staff

# Admin dashboard
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    requests = Request.objects.all().order_by('-id')
    return render(request, 'admin_dashboard.html', {'requests': requests})

# Manage requests with approval/rejection and email
@login_required
@user_passes_test(is_admin)
def manage_requests(request):
    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action_type = request.POST.get('action_type')
        req = get_object_or_404(Request, id=req_id)

        if action_type == 'approve':
            req.status = Status.APPROVED
            subject = "Request Approved"
            message = f"Hi {req.user.first_name},\n\nYour request (#{req.id}) has been approved."
        elif action_type == 'reject':
            req.status = Status.REJECTED
            subject = "Request Rejected"
            message = f"Hi {req.user.first_name},\n\nYour request (#{req.id}) has been rejected."
        else:
            messages.error(request, "Invalid action.")
            return redirect('manage_requests')

        req.updated_by = request.user
        req.save()

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [req.user.email],
            fail_silently=False,
        )

        messages.success(request, f"Request {action_type}ed and email sent.")
        return redirect('manage_requests')

    all_requests = Request.objects.all()
    return render(request, 'manage_requests.html', {'request': all_requests})

# Edit user details
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

# View user details
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'view_user.html', {'user': user, 'profile': profile})

def view_user_details(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'view_user_details.html', {'user': user, 'profile': profile})

# Employee list view
def emp_list1_view(request):
    users = User.objects.filter(profile__role='user')
    return render(request, 'emp_list1.html', {'users': users})

# Manage employees
def manage_employee_view(request):
    users = User.objects.filter(profile__role='user')
    return render(request, 'manage_employee.html', {'users': users})

# Delete user
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_employees')

# Generate payslip
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

# Employee credentials view
def employee_credentials_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'employee_credentials.html', {'user': user})

# Role search stub
def search_role(request):
    return render(request, 'search_results.html')



def update_request_status(request, req_id):
    if request.method == 'POST':
        action = request.POST.get('action_type')
        req = get_object_or_404(Request, id=req_id)

        if action == 'approve':
            req.status = Status.APPROVED
            subject = "Request Approved"
            message = f"Hi {req.user.first_name},\n\nYour request (#{req.id}) has been approved."
        elif action == 'reject':
            req.status = Status.REJECTED
            subject = "Request Rejected"
            message = f"Hi {req.user.first_name},\n\nYour request (#{req.id}) has been rejected."
        else:
            return redirect('manage_requests')

        req.save()

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [req.user.email],
            fail_silently=False,
        )

        return redirect('manage_requests')


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt  

def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
    return redirect('manage_employees')  

