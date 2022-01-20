from django.shortcuts import render
from seekapp.models import *
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.decorators import login_required


def services(request):
    return render(request,'services.html')

def home(request):
    return render (request, 'index.html')
@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def profile_jobseeker(request):
  current_user = request.jobseeker
  documents = FileUpload.objects.filter(user_id = current_user.id).all()
  return render(request,"jobseeker/profile.html",{"current_user":current_user})

def profile_employer(request):
    employer=request.user
    available=User.objects.filter(is_jobseeker= True,verified=True).all() 
    context={
        "employer":employer,
        "available":available,
    }
    return render(request,'#',context)




