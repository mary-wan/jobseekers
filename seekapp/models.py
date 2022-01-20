from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
import datetime as dt
from tinymce.models import HTMLField
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

