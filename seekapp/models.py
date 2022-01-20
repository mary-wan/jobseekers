from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
import datetime as dt
from tinymce.models import HTMLField

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


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_admin = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    profile_photo = CloudinaryField('image', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(
        unique=True, max_length=10, null=True, blank=True)
    availability = models.CharField(
        null=True, blank=True, choices=JOBSEEKER_WORKHOUR_CHOICES, max_length=20)
    salary = models.IntegerField(null=True, blank=True)
    job_category = models.CharField(
        null=True, blank=True, max_length=180, choices=JOB_CATEGORY_CHOICES)
    company = models.CharField(max_length=100, null=True, blank=True)

    def save_user(self):
        self.save()

    def update_user(self):
        self.update()

    def delete_user(self):
        self.delete()
