from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/',auth_views.LoginView.as_view(template_name = 'registration/login.html')),
    path('register/',auth_views.LoginView.as_view(template_name = 'registration/registration_form.html')),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'registration/logout.html')),
    path('services/',views.services, name='services'),
    path('jobseeker/profile/',views.profile,name='profile'),
]
