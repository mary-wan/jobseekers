from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('services/',views.services, name='services'),
    path('jobseeker/profile/',views.profile_jobseeker,name='profile'),
]
