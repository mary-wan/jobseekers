from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required

def home(request):
    return render (request, 'index.html')





