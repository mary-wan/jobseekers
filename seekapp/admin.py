import imp
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.


admin.site.register(User)
admin.site.register(JobSeeker)
admin.site.register(Employer)
admin.site.register(Contact)
admin.site.register(FileUpload)
admin.site.register(Portfolio)
admin.site.register(MpesaPayment)

