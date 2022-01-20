from django.db import models
from cloudinary.models import CloudinaryField
import datetime as dt
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='Profile')
    username=models.CharField(max_length=50)
    image=CloudinaryField('image')
    bio=models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.user.username