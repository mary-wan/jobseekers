from django.shortcuts import render
from seekapp.models import *
from django.shortcuts import render



def services(request):
    return render(request,'services.html')

# Create your views here.



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

