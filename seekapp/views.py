import json
import random
import re
from urllib.request import HTTPBasicAuthHandler
from django.shortcuts import render, redirect
from seekapp.models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import redirect, render, get_object_or_404
from seekapp.models import *
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
import os
import time
from .email import *
from django.http.response import Http404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.exceptions import ObjectDoesNotExist


def services(request):
  return render(request, 'services.html')


def options(request):
  return render(request, 'registration/options.html')


def home(request):
  return render(request, 'index.html')


@login_required
# @allowed_users(allowed_roles=['admin','jobseeker'])
def jobseeker_profile(request, id):
  jobseeker = User.objects.get(id=id)
  profile = JobSeeker.objects.get(user_id=id)  # get profile
  portfolio = Portfolio.objects.filter(user_id=id)
  # user = get_object_or_404(User, pk=user.id)
  return render(request, "employer/jobseekerview.html", {"jobseeker": jobseeker, "portfolio": portfolio, "profile": profile})
# jobseekers update profile


@login_required
def profile_jobseeker(request):
  current_user = request.user
  user = get_object_or_404(User, pk=current_user.id)
  profile = JobSeeker.objects.get(user_id=current_user.id)  # get profile
  documents = FileUpload.objects.filter(user_id=current_user.id).all()
  return render(request, "jobseeker/profile.html", {"documents": documents, "current_user": current_user, "profile": profile})


@login_required
def update_jobseeker_profile(request):
  current_user = request.user
  profile = JobSeeker.objects.get(user_id=current_user.id)
  if request.method == 'POST':
    user_form = UpdateUserProfile(request.POST,request.FILES,instance=request.user)
    jobseeker_form = UpdateJobseekerProfile(request.POST,request.FILES,instance=request.user.jobseeker)
    if user_form.is_valid() and jobseeker_form.is_valid():
      user_form.save()
      jobseeker_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('profile_jobseeker')
  else:
    user_form = UpdateUserProfile(instance=request.user)
    jobseeker_form = UpdateJobseekerProfile(instance=request.user.jobseeker)
  params = {
    'user_form':user_form,
    'jobseeker_form':jobseeker_form,
    'profile':profile
  }
  return render(request,'jobseeker/update.html',params)


#single jobseeker details
@login_required
def jobseeker_details(request,user_id):
  
    jobseeker =get_object_or_404(JobSeeker, pk = user_id)
    documents = FileUpload.objects.filter(user_id = user_id).all()
    portfolios=Portfolio.objects.filter(user_id = user_id).all()
    return render(request,)

# single jobseeker details
# @login_required
# # @allowed_users(allowed_roles=['admin'])
# def jobseeker_details(request,user_id):
#   try:
#     jobseeker =get_object_or_404(JobSeeker, pk = user_id)
#     documents = FileUpload.objects.filter(user_id = user_id).all()
#     portfolios=Portfolio.objects.filter(user_id = user_id).all()


# single jobseeker details
# @login_required
# # @allowed_users(allowed_roles=['admin'])
# def jobseeker_details(request, user_id):
#     try:
#         jobseeker = get_object_or_404(JobSeeker, pk=user_id)
#         documents = FileUpload.objects.filter(user_id=user_id).all()
#         portfolios = Portfolio.objects.filter(user_id=user_id).all()

#         return render(request, '#', {'jobseeker': jobseeker, 'documents': documents, 'portfolios': portfolios})

# delete jobseeker
@login_required
def delete_jobseeker(request,user_id):
  jobseeker = JobSeeker.objects.get(pk=user_id)
  if jobseeker:
    jobseeker.delete_user()
    messages.success(request, f'User deleted successfully!')
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#employer profle
@login_required
def employerProfile(request):
    employer = request.user
    profile = Employer.objects.get(user_id=employer.id)  # get profile
    available = User.objects.filter(is_jobseeker=True).all()
    profile = Employer.objects.filter(
        user_id=employer.id).first()  # get profile
    context = {
        "employer": employer,
        "available": available,
        'profile': profile
    }
    return render(request, 'employer/profile.html', context)


@login_required
def update_employer_profile(request):
    current_user = request.user
    profile = Employer.objects.get(
        user_id=current_user.id)  # get profile
    if request.method == 'POST':
        u_form = UpdateUserProfile(
            request.POST, request.FILES, instance=request.user)
        p_form = UpdateEmployerProfile(
            request.POST, request.FILES, instance=request.user.employer)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, 'Your Profile account has been updated successfully')
            return redirect('profile')
    else:
        u_form = UpdateUserProfile(instance=request.user)
        p_form = UpdateEmployerProfile(instance=request.user.employer)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile
    }
    return render(request, 'employer/update.html', context)

# delete employers


@login_required
def delete_employer(request,user_id):
  employer = Employer.objects.get(pk=user_id)
  if employer:
    employer.delete_user()
    messages.success(request, f'Employer deleted successfully!')
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# sigle details for jobseekers
@login_required
def single_jobseeker(request,user_id):

    jobseeker =get_object_or_404(User, pk = user_id)
    documents = FileUpload.objects.filter(user_id = user_id)
    portfolios=Portfolio.objects.filter(user_id = user_id)

# #         except ObjectDoesNotExist:
# #             raise Http404()

# #         return render(request, '#', {'documents': documents, 'jobseeker': jobseeker, "portfolios": portfolios})


def contact(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            send_contact_email(name, email)
            data = {
                'success': 'Your message has been reaceived. Thank you for contacting us, we will get back to you shortly'}
            messages.success(request, f"Message submitted successfully")
    else:
        contact_form = ContactForm()
    return render(request, 'contact.html', {'contact_form': contact_form})


@login_required
def add_portfolios(request):
    current_user = request.user
    profile = JobSeeker.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        port_form = AddPortfolio(request.POST, request.FILES)
        if port_form.is_valid():
            portfolio = port_form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            messages.success(
                request, 'Your Portfolio has been added successfully.Thank you')
            print(port_form)
            return redirect('jobseekerDash')

    else:
        port_form = AddPortfolio()
    context = {
        'port_form': port_form,
        'profile': profile
    }
    return render(request, "jobseeker/portfolio.html", context)


@login_required
# @allowed_users(allowed_roles=['admin', 'jobseeker'])
def upload_file(request):
    current_user = request.user
    profile = JobSeeker.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload = upload_form.save(commit=False)
            upload.user = request.user
            upload.save()
            messages.success(request, "File uploaded successfully")
            return redirect('jobseekerDash')
    else:
        upload_form = UploadFileForm()
    return render(request, 'jobseeker/upload_file.html', {'upload_form': upload_form, 'profile': profile})


def pdf_view(request, file_id):
    file = get_object_or_404(FileUpload, pk=file_id)
    image_data = open(
        f"/home/access/Desktop/Eloquent_JavaScript.pdf/{file.pdf}", "rb").read()
    return HttpResponse(image_data, content_type="application/pdf")


@login_required
def jobseekerPage(request):
    current_user = request.user
    documents = FileUpload.objects.filter(user_id=current_user.id).all()
    portfolios = Portfolio.objects.filter(user_id=current_user.id)
    return render(request, '#', {"documents": documents, "portfolios": portfolios})


def emp_home(request):
    return render(request, 'employer/home.html')


def jobseeker_home(request):
    return render(request, 'jobseeker/home.html')


def jobseeker_signup(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == "POST":
        form = JobseekerSignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')

    else:
        form = JobseekerSignUp()
    return render(request, "registration/register.html", {'form': form})


def employer_signup(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == "POST":
        form = EmployerSignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')

    else:
        form = EmployerSignUp()
    return render(request, "registration/register.html", {'form': form})


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
def jobseekerDash(request):
    current_user = request.user
    profile = JobSeeker.objects.get(user_id=current_user.id)
    documents = FileUpload.objects.filter(user_id=current_user.id).all()
    portfolios = Portfolio.objects.filter(user_id=current_user.id)
    return render(request, 'jobseekers/jobseeker_dashboard.html', {"documents": documents, "portfolios": portfolios, 'profile': profile})


@login_required
# @admin_only
def adminDash(request):
    all_employers = User.objects.filter(is_employer=True).all()
    all_jobseekers = User.objects.filter(is_jobseeker=True).all()
    verified_jobseekers = User.objects.filter(
        verified=True, is_jobseeker=True).all()
    unverified_jobseekers = User.objects.filter(
        verified=False, is_jobseeker=True).all()
    verified_employers = User.objects.filter(
        verified=True, is_employer=True).all()
    unverified_employers = User.objects.filter(
        verified=False, is_employer=True).all()
    return render(request, 'admin/admin_dashboard.html', {"unverified_employers": unverified_employers, "verified_employers": verified_employers, "all_employers": all_employers, 'verified_jobseekers': verified_jobseekers, 'unverified_jobseekers': unverified_jobseekers, 'all_jobseekers': all_jobseekers})


@login_required
def employerDash(request):
    current_user = request.user
    profile = Employer.objects.get(user_id=current_user.id)
    job_seekers = User.objects.filter(is_jobseeker=True).all()
    # potential = JobSeeker.objects.all()
    employer = User.objects.all()
    if request.method == 'POST':
        mpesa_form = PaymentForm(
            request.POST, request.FILES, instance=request.user)
        if mpesa_form.is_valid():
            mpesa_form.save()
            messages.success(
                request, 'Your Payment has been made successfully')
            return redirect('employerDash')
    else:
        mpesa_form = PaymentForm(instance=request.user)

    context = {
        # "potential": potential,
        "job_seekers": job_seekers,
        "employer": employer,
        'profile': profile,
        'mpesa_form':mpesa_form
    }
    return render(request, 'employers/employer_dashboard.html', context)


# @login_required
# def employerDash(request):
#     user = request.user
#     job_seekers = User.objects.filter(
#         is_verified=True, is_jobseeker=True).all()
#     employer = User.objects.all()

#     context = {
#         "job_seekers": job_seekers,
#         "employer": employer,
#     }
#     return render(request, 'employers/employer_dashboard.html', context)


@login_required
def employerPayment(request):
    current_user = request.user
    if request.method == 'POST':
        mpesa_form = PaymentForm(
            request.POST, request.FILES, instance=request.user)
        if mpesa_form.is_valid():
            mpesa_form.save()
            messages.success(
                request, 'Your Payment has been made successfully')
            return redirect('employerDash')
    else:
        mpesa_form = PaymentForm(instance=request.user)
    context = {
        'mpesa_form': mpesa_form,
    }
    return render(request, 'employers/paymentform.html', context)

# Mpesa


def getAccessToken(request):
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    # r = requests.get(api_URL, auth=HTTPBasicAuthHandler(
    #     consumer_key, consumer_secret))
    mpesa_access_token = json.loads(re.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)


def success(request):
    time.sleep(10)
    return HttpResponseRedirect("/employerDash")

    return render('mpesa/success.html')


def stk_push_callback(request):
    data = request.body


def search_jobseekers(request):
    current_user = request.user
    profile = Employer.objects.get(user_id=current_user.id)
    if 'job_category' in request.GET and request.GET["job_category"]:
        search_term = request.GET.get("job_category")
        searched_jobseekers = JobSeeker.search_jobseekers_by_job_category(
            search_term)
        message = f"{search_term}"

        return render(request, 'employer/search.html', {"message": message, "jobseekers": searched_jobseekers,'profile':profile})

    else:
        message = 'You have not searched for any term'
        return render(request, 'employer/search.html', {"message": message,})


def contact(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            send_contact_email(name, email)
            data = {
                'success': 'Your message has been reaceived. Thank you for contacting us, we will get back to you shortly'}
            messages.success(request, f"Message submitted successfully")
    else:
        contact_form = ContactForm()
    return render(request, 'contact.html', {'contact_form': contact_form})


@login_required
def upload_file(request):
    if request.method == 'POST':
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload = upload_form.save(commit=False)
            upload.user = request.user
            upload.save()
            messages.success(request, "File uploaded successfully")
            return redirect('jobseekerDash')
    else:
        upload_form = UploadFileForm()
    return render(request, 'jobseeker/upload_file.html', {'upload_form': upload_form})


def pdf_view(request, file_id):
    file = get_object_or_404(FileUpload, pk=file_id)
    image_data = open(
        f"/home/access/Desktop/Eloquent_JavaScript.pdf/{file.pdf}", "rb").read()
    return HttpResponse(image_data, content_type="application/pdf")


@login_required
def jobseekerPage(request):
    current_user = request.user
    documents = FileUpload.objects.filter(user_id=current_user.id).all()
    portfolios = Portfolio.objects.filter(user_id=current_user.id)
    return render(request, '#', {"documents": documents, "portfolios": portfolios})


def emp_home(request):
    return render(request, 'employer/home.html')


def jobseeker_home(request):
    return render(request, 'jobseeker/home.html')


def search_by_category(request):
    if 'job_category' in request.GET and request.GET["job_category"]:
        search_term = request.GET.get("job_category")
        searched_jobseekers = JobSeeker.search_jobseekers_by_job_category(
            search_term)
        message = f"{search_term}"

        return render(request, 'job-cat/search.html', {"message": message, "jobseekers": searched_jobseekers})

    else:
        message = 'You have not searched for any term'
        return render(request, 'job-cat/search.html', {"message": message})
