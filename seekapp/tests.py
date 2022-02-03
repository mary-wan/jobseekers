from django.core.mail import message
from django.test import TestCase
from .models import *

# Create your tests here.
class JobseekerTestClass(TestCase):
    def setUp(self):
        self.user = User(
            id=1,
            username='Mary',
            email= 'mary@gmail.com',
            first_name='Mary',
            last_name='Wan',
            is_jobseeker=True)
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def tearDown(self):
        self.user.delete_user()

    def test_save_method(self):
        self.user.save_user()
        users  = User.objects.all()
        self.assertTrue(len(users)>0)

    def test_get_all_users(self):
        users = User.get_all_users()
        self.assertTrue(len(users)>0)

    def test_get_user_id(self):
        users= User.get_user_id(self.user.id)
        self.assertTrue(len(users) == 1)

def test_update_user(self):
        self.user.save_user()
        user = User.update_user(
            self.user.id, 
            'Maria',
            'mary@gmail.com',
            'Maria',
            'Wan',
            True)
        user_item = user.objects.filter(id = self.user.id)
        print(user_item)
        self.assertTrue(user.name == 'Maria')
        
        
class FileUploadTestClass(TestCase):

    def setUp(self):
        self.file_upload = FileUpload(name='Test FileUpload')

    def test_save_method(self):
        self.file_upload.save()
        file_upload = FileUpload.objects.all()
        self.assertTrue(len(file_upload) > 0)
        
class ContactTestClass(TestCase):
    # Set up Method
    def setUp(self):
        self.contact = Contact(
            name='Anipher Chelsea', 
            email='chelsea.ayoo@moringaschool.com',
            message= 'Hello Jobslux. Will my employer account be activated immediately I make the payment?')
        self.contact.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.contact, Contact))

    def tearDown(self):
        self.contact.delete_contact()

    def test_save_method(self):
        self.contact.save_contact()
        contacts  = Contact.objects.all()
        self.assertTrue(len(contacts)>0)
        
class PortfolioTestClass(TestCase):
    # Set up Method
    def setUp(self):
        self.user = User(id=2,username='Moringa',email='moringa@gmail.com',bio='',)
        self.user.save_user()

        self.portfolio = Portfolio(name='CV', link='moringa_portfolio.com',user= self.user)
        self.portfolio.save()


    def test_instance(self):
        self.assertTrue(isinstance(self.portfolio, Portfolio))

    def tearDown(self):
        self.portfolio.delete_portfolio()

    def test_save_method(self):
        self.portfolio.save_portfolio()
        portfolios  = Portfolio.objects.all()
        self.assertTrue(len(portfolios)>0)

    def test_get_all_portfolios(self):
        portfolios = Portfolio.get_all_portfolios()
        self.assertTrue(len(portfolios)>0)

    def test_get_portfolio_id(self):
        portfolios= Portfolio.get_portfolio_id(self.portfolio.id)
        self.assertTrue(len(portfolios) == 1)

    def test_update_portfolio(self):
        self.portfolio.save_portfolio()
        portfolio = Portfolio.update_portfolio( self.portfolio.id, 'test update', 'portfolio test')
        portfolio_item = portfolio.objects.filter(id = self.portfolio.id)
        print(portfolio_item)
        self.assertTrue(portfolio.name == 'test update')