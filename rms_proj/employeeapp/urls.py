from employeeapp import views
from django.urls import path


urlpatterns = [


    path('change_password/', views.change_password, name='change_password'),
    path('request_overview/', views.request_overview, name='request_overview'),
    path('user_details/', views.user_details, name='user_details'),
    path('submit_request/', views.submit_request, name='submit_request'),
    path('user_dashboard/', views.user_dashboard, name="user_dashboard"),
    
]