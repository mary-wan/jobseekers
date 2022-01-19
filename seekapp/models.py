from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

JOBSEEKER_AVAILABILITY = (
    ('Full Time', "Full Time"),
    ('Part Time', "Part Time"),
)

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []#removes email from REQUIRED_FIELDS
    is_admin = models.BooleanField(default=False)