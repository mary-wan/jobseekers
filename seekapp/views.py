from django.shortcuts import redirect, render
from seekapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *


def services(request):
    return render(request,'services.html')

def home(request):
    return render (request, 'index.html')

@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def profile_jobseeker(request):
  current_user = request.user
  profile = JobSeeker.objects.filter(user_id=current_user.id).first()  # get profile
  documents = FileUpload.objects.filter(user_id = current_user.id).all()
  return render(request,"jobseeker/profile.html",{"documents":documents,"current_user":current_user,"profile":profile})

@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def update_jobseeker_profile(request):
  if request.method == 'POST':
    user_form = UpdateUserProfile(request.POST,request.FILES,instance=request.user)
    jobseeker_form = UpdateJobseekerProfile(request.POST,instance=request.user)
    if user_form.is_valid() and jobseeker_form.is_valid():
      user_form.save()
      jobseeker_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('#')
  else:
    user_form = UpdateUserProfile(instance=request.user)
    jobseeker_form = UpdateJobseekerProfile(instance=request.user) 
  params = {
    'user_form':user_form,
    'jobseeker_form':jobseeker_form
  }
  return render(request,'jobseekers/update.html',params)

def profile_employer(request):
    employer=request.user
    available=User.objects.filter(is_jobseeker= True,verified=True).all() 
    context={
        "employer":employer,
        "available":available,
    }
    return render(request,'#',context)




