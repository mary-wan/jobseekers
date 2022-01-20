from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


# Registration form
class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
class UpdateJobseekerProfile(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ('job_category','availability', 'salary')

class UpdateUserProfile(forms.ModelForm):
  email = forms.EmailField()
  class Meta:
    model = JobSeeker
    fields = ['firstName', 'lastName','email','contact','location', 'profile_photo','bio']

class ContactForm(forms.ModelForm):
    class Meta:
      model = Contact
      fields = ['name','email','message']

class AddPortfolio(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name','link',  )
        
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('name','pdf')
        
class UpdateEmployerProfile(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('company_name',  )

