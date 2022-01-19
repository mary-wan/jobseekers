from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request,'jobseeker/index.html')


def profile(request):
    return render(request, "jobseeker/profile.html", {"profile": profile,})

