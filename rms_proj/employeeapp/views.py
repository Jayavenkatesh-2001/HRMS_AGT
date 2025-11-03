from django.shortcuts import render
from rms_app.models import Request
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect, render
from rms_app.forms import SignInForm, RequestForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, login as auth_login
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST


# Create your views here.
def user_dashboard(request):
    requests = Request.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'requests': requests})


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from rms_app.forms import RequestForm


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




from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def user_dashboard(request):
    user_requests = Request.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {
        'requests': user_requests
    })
    
    
   
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone


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


def change_password(request):
    return render(request, 'change_password.html')




def user_details(request):
    user = request.user
    # render user details
    return render(request, 'user_details.html', {'user': user})

