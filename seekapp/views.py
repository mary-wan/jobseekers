from django.shortcuts import render,redirect
from seekapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *


def services(request):
    return render(request,'services.html')

def home(request):
    return render (request, 'index.html')


def profile_jobseeker(request):
  current_user = request.user
  return render(request,'#',{"current_user":current_user})

def profile_employer(request):
    employer=request.user
    available=User.objects.filter(is_jobseeker= True,verified=True).all() 
    context={
        "employer":employer,
        "available":available,
    }
    return render(request,'#',context)

def profile(request):
    return render(request, "jobseeker/profile.html", {"profile": profile,})

def emp_home(request):
    return render (request, 'employer/home.html')

def jobseeker_home(request):
    return render (request, 'jobseeker/home.html')

def jobseeker_signup(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method=="POST":
        form = JobseekerSignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('jobseeker_home')
            
    else:
        form = JobseekerSignUp()
    return render(request,"registration/register.html",{'form':form})


def employer_signup(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method=="POST":
        form = EmployerSignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('emp_home')
            
    else:
        form = EmployerSignUp()
    return render(request,"registration/register.html",{'form':form})


