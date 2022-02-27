from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def login(request):
    return render(request, 'login/logIn.html')

def signup(request):
    return render(request, 'login/SignUp.html')

def home(request):
    return render(request, 'profile/index.html')

def profile(request):
    return HttpResponse('This is the profile page')


