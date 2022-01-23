from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('profile/', views.profile_jobseeker, name = 'profile'),
    path('services/',views.services, name='services'),
    path('jobseeker/profile/',views.profile_jobseeker,name='profile'),
    path('signup/jobseeker/', views.jobseeker_signup,name='jobseeker_signup'),
    path('signup/employer/', views.employer_signup,name='employer_signup'),
    path('employer/home/',views.emp_home, name='emp_home'),
    path('jobseeker/home/',views.jobseeker_home, name='jobseeker_home'),
    path('contact_us/',views.contact, name='contact_us'),
]
