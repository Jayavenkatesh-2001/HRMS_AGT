from adminapp import views
from django.urls import path


urlpatterns = [
    path('add_employee/', views.add_employee_view, name='add_employee'),

    
    
    
    
   
    path('employee_list/', views.employee_list, name='employee_list'),
    
   
    
    path('view_user_superuser/<int:user_id>/', views.view_user_superuser, name='view_user_superuser'),
    
    
    

   
    path('edit_user_superuser/<int:user_id>/', views.edit_user_superuser, name='edit_user_superuser'),
    path('employee_credentials_superuser/<int:user_id>/', views.employee_credentials_superuser, name='employee_credentials_superuser'),
    path('manage_employee_superuser/', views.manage_employee_superuser, name='manage_employee_superuser'),
    
    path('delete_user_superuser/<int:user_id>/', views.delete_user_superuser, name='delete_user_superuser'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('check_email/', views.check_email_view, name='check_email'),
    path('check_emp_id/', views.check_emp_id, name='check_emp_id'),

    
]





