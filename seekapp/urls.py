from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views as app_views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('services/',views.services, name='services'),
    path('jobseeker/profile/',views.profile,name='profile'),
    path('jobseekerDash/',app_views.jobseekerDash,name='jobseekerDash'),
    path('dashboard',app_views.dashboard,name='dashboard'),
    path('admin_dashboard/',app_views.adminDash,name='admin_dashboard'),
    path('employerDash/',app_views.employerDash,name='employerDash'),
    path('search_jobseekers/',views.search_jobseekers,name='search_jobseekers'),
]
