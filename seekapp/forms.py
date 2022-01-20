from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import *


# Registration form
class JobseekerSignUp(UserCreationForm):
    first_name= forms.CharField(label='First Name' ,error_messages={'required': 'Please enter your first name'})
    last_name= forms.CharField(label='Last Name',error_messages={'required': 'Please enter your last name'})
    email= forms.EmailField(label='Email Address' ,help_text='Format: 123@gmail.com, 456@yahoo.com',error_messages={'required': 'Please enter your email address'})

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields=['first_name','last_name','username','email','password1','password2']

        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_jobseeker=True
        user.save()
        jobseeker = JobSeeker.objects.create(user=user)
        jobseeker.first_name = self.cleaned_data.get('first_name')
        jobseeker.last_name = self.cleaned_data.get('last_name')
        jobseeker.email = self.cleaned_data.get('email')
        return user
    
    
CustomUser._meta.get_field('email')._unique=True


class EmployerSignUp(UserCreationForm):
    first_name= forms.CharField(label='First Name' ,error_messages={'required': 'Please enter your first name'})
    last_name= forms.CharField(label='Last Name',error_messages={'required': 'Please enter your last name'})
    email= forms.EmailField(label='Email Address' ,help_text='Format: 123@gmail.com, 456@yahoo.com',error_messages={'required': 'Please enter your email address'})

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields=['first_name','last_name','username','email','password1','password2']

        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employer=True
        user.save()
        employer = Employer.objects.create(user=user)
        employer.first_name = self.cleaned_data.get('first_name')
        employer.last_name = self.cleaned_data.get('last_name')
        employer.email = self.cleaned_data.get('email')
        return user
    
CustomUser._meta.get_field('email')._unique=True
       
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = "__all__"
