import imp
from django.contrib import admin
from .forms import CustomUserCreationForm
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User role',
            {
                'fields':(
                    'is_admin',
                    'is_employer',
                    'is_jobseeker',
                    'is_verified',
                )
            }
        )
    )
    
admin.site.register(CustomUser, CustomUserAdmin)
