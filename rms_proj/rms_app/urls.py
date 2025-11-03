from rms_app import views
from django.urls import path

urlpatterns = [
    path('',views.aptsol_global_view, name='aptsol_global'),
    path('Signin/', views.Signin_view, name='Signin'),
    path('login', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('home', views.home, name='home'),



    

    
]



    

