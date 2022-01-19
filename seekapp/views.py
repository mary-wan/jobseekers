from django.shortcuts import render
from seekapp.models import *
from django.shortcuts import render


# Create your views here.



def profile_jobseeker(request):
  current_user = request.user
  return render(request,'#',{"current_user":current_user})


