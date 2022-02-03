from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField
from django.contrib.auth.models import PermissionsMixin
from django.db import models
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


class User(AbstractUser):
    USERNAME_FIELD = 'username'
    is_admin = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def save_user(self):
        self.save()

    def update_user(self):
        self.update()

    def delete_user(self):
        self.delete()


class JobSeeker(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    # firstName = models.CharField(max_length=100, null=True, blank=True)
    # lastName = models.CharField(max_length=100, null=True, blank=True)
    profile_photo = CloudinaryField('image', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(
        unique=True, max_length=30, null=True, blank=True)
    availability = models.CharField(
        null=True, blank=True, choices=JOBSEEKER_WORKHOUR_CHOICES, max_length=20)
    salary = models.IntegerField(null=True, blank=True)
    job_category = models.CharField(
        null=True, blank=True, max_length=180, choices=JOB_CATEGORY_CHOICES)
    email = models.CharField(max_length=50, null=True)

    def save_jobseeker(self):
        self.save()

    def delete_jobseeker(self):
        self.delete()

    @classmethod
    def update_jobseeker(self):
        self.update()

    @classmethod
    def search_jobseekers_by_job_category(cls, job_category):
        jobseekers = JobSeeker.objects.filter(
            job_category__icontains=job_category)
        return jobseekers

    # def __str__(self):
    #     return self.username


class Employer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    # firstName = models.CharField(max_length=100, null=True, blank=True)
    # lastName = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=50, null=True)
    profile_photo = CloudinaryField('image', null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)

    def save_employer(self):
        self.save()

    def update_employer(self):
        self.update()

    def delete_employer(self):
        self.delete()


class FileUpload(models.Model):
    name = models.CharField(max_length=100)
    pdf= models.FileField(upload_to='static/',null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='documents')

    def save_upload(self):
        self.save()

    def delete_upload(self):
        self.delete()

    @classmethod
    def update_upload(cls, id, name, pdf, user):
        update = cls.objects.filter(id=id).update(
            name=name, pdf=pdf, user=user)
        return update

    @classmethod
    def get_all_uploads(cls):
        uploads = cls.objects.all()
        return uploads

    @classmethod
    def get_upload_id(cls, id):
        upload_id = cls.objects.filter(id=id).all()
        return upload_id

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='portfolio')
    name = models.CharField(max_length=50)
    link = models.URLField(max_length=555)

    def save_portfolio(self):
        self.save()

    def delete_portfolio(self):
        self.delete()

    @classmethod
    def update_portfolio(cls, id, name, link, user):
        update = cls.objects.filter(id=id).update(
            name=name, link=link, user=user)
        return update

    @classmethod
    def get_all_portfolios(cls):
        portfolios = cls.objects.all()
        return portfolios

    @classmethod
    def get_portfolio_id(cls, id):
        portfolio_id = cls.objects.filter(id=id).all()
        return portfolio_id

    def __str__(self):
        return self.name

    def delete_upload(self):
        self.delete()


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.TextField()

    def save_contact(self):
        self.save()

    def delete_contact(self):
        self.delete()

    def __str__(self):
        return self.name


class Subscribe(models.Model):
    first_name = models.CharField(max_length=144, null=True, blank=True)
    last_name = models.CharField(max_length=144, null=True, blank=True)
    contact = models.CharField(max_length=30)


# class AccessToken(models.Model):
#     token = models.CharField(max_length=30)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         get_latest_by = 'created_at'

#     def __str__(self):
#         return self.token


# accepted/completed transactions


class MpesaPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact = models.TextField()

    class Meta:
        verbose_name = "Mpesa Payment"
        verbose_name_plural = "Mpesa Payments"

    def __str__(self):
        return self.first_name





