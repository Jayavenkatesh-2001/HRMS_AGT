from hrapp import views
from django.urls import path


urlpatterns = [
    path('admin_dashboard/',views.admin_dashboard, name="admin_dashboard"),
    path('update_request_status/<int:req_id>/', views.update_request_status, name="update_request_status"),
    path('edit_user/<int:user_id>/', views.edit_user_detail, name='edit_user'),
    path('emp_list1/', views.emp_list1_view, name='emp_list1'),
    path('manage_employee/', views.manage_employee_view, name='manage_employee'),
    
    path('generate_payslip/<int:user_id>/', views.generate_payslip, name='generate_payslip'),
     path('manage_requests/', views.manage_requests, name='manage_requests'),
    path('view_user_details/', views.view_user_details, name='view_user_details'),
    path('update_request_status/<int:req_id>/', views.update_request_status, name='update_request_status'),
    path('view_user/<int:user_id>/', views.view_user, name='view_user'),
    path('employee_credentials/<int:user_id>/', views.employee_credentials_view, name='employee_credentials'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('search_role/', views.search_role, name='search_role'),
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
]
