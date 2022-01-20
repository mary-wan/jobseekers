from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
import datetime as dt
from tinymce.models import HTMLField, URLField
from django.contrib.auth.models import PermissionsMixin

# Create your models here.



JOBSEEKER_WORKHOUR_CHOICES = (

    ('Full Time', "Full Time"),
    ('Part Time', "Part Time"),
)




JOB_CATEGORY_CHOICES = (
    ('UI/UX-Designer', "UI/UX-Designer"),
    ('Data Scientist', "Data Scientist"),
    ('IT support technician', "IT support technician"),
    ('Software developer', "Software developer"),
    ('Systems analyst', "Systems analyst"),
    ('Computer service and repair technician',
     "Computer service and repair technician"),
    ('Solution architect', "Solution architect"),
    ('Network manager', "Network manager"),
)


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    is_admin = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def save_user(self):
        self.save()

    def update_user(self):
        self.update()

    def delete_user(self):
        self.delete()
        
class JobSeeker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    firstName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    profile_photo = CloudinaryField('image', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(unique=True, max_length=10, null=True, blank=True)
    availability = models.CharField(
        null=True, blank=True, choices=JOBSEEKER_WORKHOUR_CHOICES, max_length=20)
    salary = models.IntegerField(null=True, blank=True)
    job_category = models.CharField(
        null=True, blank=True, max_length=180, choices=JOB_CATEGORY_CHOICES)
    email = models.EmailField(unique=True)
    
    def save_jobseeker(self):
        self.save()

    def update_jobseeker(self):
        self.update()

    def delete_jobseeker(self):
        self.delete()
        
        
class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    firstName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    profile_photo = CloudinaryField('image', null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    job_category = models.CharField(
        null=True, blank=True, max_length=180, choices=JOB_CATEGORY_CHOICES)
    
    def save_employer(self):
        self.save()

    def update_employer(self):
        self.update()

    def delete_employer(self):
        self.delete()
        
class FileUpload(models.Model):
    name = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='documents/pdf/')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='documents')

    def save_upload(self):
        self.save()

    def delete_upload(self):
        self.delete()
    
    def __str__(self):
        return self.name
    
class Portfolio(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='portfolio')
    name = models.CharField(max_length=50)
    link=models.URLField(max_length=555)

    def save_portfolio(self):
        self.save()

    def delete_portfolio(self):
        self.delete()
        
    def __str__(self):
        return self.name
    
