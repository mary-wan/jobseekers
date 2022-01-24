from django.shortcuts import render,redirect
from seekapp.models import *
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import redirect, render,get_object_or_404
from seekapp.models import *
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
import os
from .email import *
from django.http.response import Http404
from django.http import HttpResponse,HttpResponseRedirect,Http404,JsonResponse
from django.core.exceptions import ObjectDoesNotExist


def services(request):
    return render(request,'services.html')

def home(request):
    return render (request, 'index.html')


@login_required
# @allowed_users(allowed_roles=['admin','jobseeker'])
def profile_jobseeker(request):
  current_user = request.user
  profile = JobSeeker.objects.filter(user_id=current_user.id).first()  # get profile
  documents = FileUpload.objects.filter(User_id = current_user.id).all()
  return render(request,"jobseeker/profile.html",{"documents":documents,"current_user":current_user,"profile":profile})


#jobseekers update profile
@login_required
# @allowed_users(allowed_roles=['admin','jobseeker'])
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


#single jobseeker details
@login_required
@allowed_users(allowed_roles=['admin'])
def jobseeker_details(request,user_id):
  try:
    jobseeker =get_object_or_404(JobSeeker, pk = user_id)
    documents = FileUpload.objects.filter(user_id = user_id).all()
    portfolios=Portfolio.objects.filter(user_id = user_id).all()

  except ObjectDoesNotExist:
    raise Http404()

  return render(request,'#',{'jobseeker':jobseeker,'documents':documents,'portfolios':portfolios})

#delete jobseeker


#employer profle
@login_required
# @allowed_users(allowed_roles=['admin','employer'])
def employerProfile(request):
    employer=request.user
    available=User.objects.filter(is_jobseeker= True).all() 
    context={
        "employer":employer,
        "available":available,
    }
    return render(request,'employer/profile.html',context)

@login_required
# @allowed_users(allowed_roles=['admin','employer'])
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

#delete employers
@login_required
@allowed_users(allowed_roles=['admin'])
def delete_employer(request,user_id):
  employer = Employer.objects.get(pk=user_id)
  if employer:
    employer.delete_user()
    messages.success(request, f'Employer deleted successfully!')
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
      return redirect('#')

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
            return redirect('#')
    else:
        upload_form = UploadFileForm()
    return render(request, 'jobseekers/upload_file.html', {'upload_form': upload_form})

def pdf_view(request,file_id):
    file =get_object_or_404(FileUpload, pk = file_id)
    image_data = open(f"/home/access/Desktop/Eloquent_JavaScript.pdf/{file.pdf}", "rb").read()
    return HttpResponse(image_data, content_type="application/pdf")

@login_required
# @allowed_users(allowed_roles=['admin','jobseeker'])
def jobseekerPage(request):
    current_user = request.user
    documents = FileUpload.objects.filter(user_id = current_user.id).all()
    portfolios=Portfolio.objects.filter(user_id = current_user.id)
    return render(request,'#',{"documents":documents,"portfolios":portfolios})


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

#jobseekers update profile
@login_required
# @allowed_users(allowed_roles=['admin','jobseeker'])
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
# @allowed_users(allowed_roles=['admin','employer'])
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

@login_required
def dashboard(request):
    current = request.user
    if current.is_employer:
        return redirect('employerDash/')
    elif current.is_admin:
        return redirect('admin_dashboard')
    else: 
        return redirect('jobseekerDash/')

@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def jobseekerDash(request):
    current_user = request.user
    documents = FileUpload.objects.filter(user_id = current_user.id).all()
    portfolios=Portfolio.objects.filter(user_id = current_user.id)
    return render(request,'jobseekers/jobseeker_dashboard.html',{"documents":documents,"portfolios":portfolios})

@login_required
@admin_only
def adminDash(request):
    all_employers= User.objects.filter(is_employer=True).all()
    all_jobseekers = User.objects.filter(is_jobseeker=True).all()
    verified_jobseekers = User.objects.filter(verified=True,is_jobseeker = True).all()
    unverified_jobseekers = User.objects.filter(verified = False,is_jobseeker = True).all()
    verified_employers = User.objects.filter(verified=True,is_employer = True).all()
    unverified_employers = User.objects.filter(verified = False,is_employer = True).all()
    return render(request,'admin/admin_dashboard.html',{"unverified_employers":unverified_employers  ,"verified_employers":verified_employers  ,"all_employers":all_employers ,'verified_jobseekers':verified_jobseekers,'unverified_jobseekers':unverified_jobseekers,'all_jobseekers':all_jobseekers})

@login_required
@allowed_users(allowed_roles=['admin','employer'])
def employerDash(request):
    user = request.user
    job_seekers = User.objects.filter(verified = True,is_jobseeker = True).all()
    employer=User.objects.all()
    
    context={
        "job_seekers":job_seekers,
        "employer":employer,
    }
    return render(request,'employers/employer_dashboard.html',context)

def search_jobseekers(request):
  if 'job_category' in request.GET and request.GET["job_category"]:
    search_term = request.GET.get("job_category")
    searched_jobseekers = User.search_jobseekers_by_job_category(search_term)
    message = f"{search_term}"

    return render(request, 'employers/search.html', {"message":message,"jobseekers":searched_jobseekers})

  else:
    message = 'You have not searched for any term'
    return render(request, 'employer/search.html', {"message":message})

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

@login_required
# @allowed_users(allowed_roles=['admin','jobseeker'])
def jobseekerPage(request):
    current_user = request.user
    documents = FileUpload.objects.filter(user_id = current_user.id).all()
    portfolios=Portfolio.objects.filter(user_id = current_user.id)
    return render(request,'#',{"documents":documents,"portfolios":portfolios})


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


