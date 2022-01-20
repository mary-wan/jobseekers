from django.shortcuts import redirect, render,get_object_or_404
from seekapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
import os
from .email import *
from django.http.response import Http404
from django.http import HttpResponse,HttpResponseRedirect,Http404,JsonResponse


def services(request):
    return render(request,'services.html')

def home(request):
    return render (request, 'index.html')

#jobseekers profile
@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def profile_jobseeker(request):
  current_user = request.user
  profile = JobSeeker.objects.filter(user_id=current_user.id).first()  # get profile
  documents = FileUpload.objects.filter(user_id = current_user.id).all()
  return render(request,"jobseeker/profile.html",{"documents":documents,"current_user":current_user,"profile":profile})

#jobseekers update profile
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

#employer profle
@login_required
@allowed_users(allowed_roles=['admin','employer'])
def employerProfile(request):
    employer=request.user
    available=User.objects.filter(is_jobseeker= True,verified=True).all() 
    context={
        "employer":employer,
        "available":available,
    }
    return render(request,'#',context)

@login_required
@allowed_users(allowed_roles=['admin','employer'])
def update_employer(request):
  if request.method == 'POST':
    u_form = UpdateUserProfile(request.POST,request.FILES,instance=request.user)
    p_form = UpdateEmployerProfile(request.POST,instance=request.user)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('#')
  else:
    u_form = UpdateUserProfile(instance=request.user)
    p_form = UpdateEmployerProfile(instance=request.user) 
  context = {
    'u_form':u_form,
    'p_form':p_form
  }
  return render


def contact(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    if request.method == 'POST':
      contact_form = ContactForm(request.POST)
      if contact_form.is_valid():
        contact_form.save()
        send_contact_email(name, email)
        data = {'success': 'Your message has been reaceived. Thank you for contacting us, we will get back to you shortly'}
        messages.success(request, f"Message submitted successfully")
    else:
      contact_form = ContactForm()
    return render(request,'contact.html',{'contact_form':contact_form})

@login_required
def add_portfolios(request):
  if request.method == 'POST':
    port_form=AddPortfolio(request.POST,request.FILES)
    if port_form.is_valid():
      portfolio = port_form.save(commit=False)
      portfolio.user = request.user
      portfolio.save()
      messages.success(request,'Your Portfolio has been added successfully.Thank you')
      print(port_form)
      return redirect('jobseekerDash')

  else:
    port_form = AddPortfolio()
  context = {
    'port_form': port_form,
    }
  return render(request,"jobseekers/portfolio.html",context)

@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def upload_file(request):
    if request.method == 'POST':
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload = upload_form.save(commit=False)
            upload.user = request.user
            upload.save()
            messages.success(request,"File uploaded successfully")
            return redirect('jobseekerDash')
    else:
        upload_form = UploadFileForm()
    return render(request, 'jobseekers/upload_file.html', {'upload_form': upload_form})

def pdf_view(request,file_id):
    file =get_object_or_404(FileUpload, pk = file_id)
    image_data = open(f"/home/access/Desktop/Eloquent_JavaScript.pdf/{file.pdf}", "rb").read()
    return HttpResponse(image_data, content_type="application/pdf")



