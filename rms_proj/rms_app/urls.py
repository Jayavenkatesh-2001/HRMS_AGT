from . import views
from django.urls import path

urlpatterns = [
    path('',views.aptsol_global_view, name='aptsol_global'),
    path('Signin/', views.Signin_view, name='Signin'),
    path('login', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('request/',views.submit_request, name='submit_request'),
    path('admin_dashboard/',views.admin_dashboard, name="admin_dashboard"),
    path('user_dashboard/', views.user_dashboard, name="user_dashboard"),
    
    path('update_request_status/<int:req_id>/', views.update_request_status, name="update_request_status"),
    path('home', views.home, name='home'),
    path('about/', views.about, name='about'),
# New URL pattern
    path('add_employee/', views.add_employee_view, name='add_employee'),

    path('employee_credentials/<int:user_id>/', views.employee_credentials_view, name='employee_credentials'),
    path('emp_list1/', views.emp_list1_view, name='emp_list1'),
    path('edit_user/<int:user_id>/', views.edit_user_detail, name='edit_user'),
    path('manage_requests/', views.manage_requests, name='manage_requests'),
    path('manage_employees/', views.manage_employee_view, name='manage_employees'),
    path('change_password/', views.change_password, name='change_password'),
    path('request_overview/', views.request_overview, name='request_overview'),
    path('user_details/', views.user_details, name='user_details'),
    path('employee_list/', views.employee_list, name='employee_list'),
    path('manage_employees/', views.manage_employees, name='manage_employees'),
    path('add_employee/', views.add_employee_view, name='add_employee'),
    path('view_user/<int:user_id>/', views.view_user, name='view_user'),
    path('view_user_superuser/<int:user_id>/', views.view_user_superuser, name='view_user_superuser'),
    path('view_user_details/', views.view_user_details, name='view_user_details'),
    path('update_request_status/<int:req_id>/', views.update_request_status, name='update_request_status'),
    path('submit_request/', views.submit_request, name='submit_request'),
    

   
    path('edit_user_superuser/<int:user_id>/', views.edit_user_superuser, name='edit_user_superuser'),
    path('employee_credentials_superuser/<int:user_id>/', views.employee_credentials_superuser, name='employee_credentials_superuser'),
    path('manage_employee_superuser/', views.manage_employee_superuser, name='manage_employee_superuser'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete_user_superuser/<int:user_id>/', views.delete_user_superuser, name='delete_user_superuser'),
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('search/', views.search, name='search'),
    path('search_role', views.search_role, name='search_role'),
    path('generate_payslip/<int:user_id>/', views.generate_payslip, name='generate_payslip'),
    # path('update_request_status/', views.update_request_status, name='update_request_status'),


    

    
]



    

