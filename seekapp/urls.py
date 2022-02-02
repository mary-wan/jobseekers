from http import server
from unicodedata import name
from django import urls
from django.urls import URLPattern, URLResolver, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views as app_views

urlpatterns = [
    path('', views.home, name='home'),
    # path('profile/', views.profile_jobseeker, name = 'profile'),
    path('services/', views.services, name='services'),
    path('register/options/', views.options, name='options'),
    path('jobseeker/profile/', views.profile_jobseeker, name='profile_jobseeker'),
    path('jobseeker/profile/<int:id>',
         views.jobseeker_profile, name='jobseeker_profile'),
    path('update_jobseeker_profile/', views.update_jobseeker_profile,
         name='update_jobseeker_profile'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('add_portfolio/', views.add_portfolios, name='add_portfolio'),
    path('employer/profile/', views.employerProfile, name='profile'),
    path('update_employer_profile/',
         views.update_employer_profile, name='update_employer'),
    path('signup/jobseeker/', views.jobseeker_signup, name='jobseeker_signup'),
    path('signup/employer/', views.employer_signup, name='employer_signup'),
    path('employer/home/', views.emp_home, name='emp_home'),
    path('jobseeker/home/', views.jobseeker_home, name='jobseeker_home'),
    path('contact_us/', views.contact, name='contact_us'),
    path('jobseekerDash/', app_views.jobseekerDash, name='jobseekerDash'),
    path('dashboard/', app_views.dashboard, name='dashboard'),
    path('admin_dashboard/', app_views.adminDash, name='admin_dashboard'),
    path('employerDash/', app_views.employerDash, name='employerDash'),
    path('employerPayment/', app_views.employerPayment, name='employerPayment'),
    path('search_jobseekers/', views.search_jobseekers, name='search_jobseekers'),
    path('search_category/', views.search_by_category, name='search_categories'),
]
