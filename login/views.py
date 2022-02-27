from django import http
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
import random

# Create your views here.

def login(request):
    return render(request, 'login/logIn.html')


def OTP(request):
    if request.method == "POST":
        # OTP VALUE
        val1 = request.POST['val1']
        val2 = request.POST['val2']
        val3 = request.POST['val3']
        val4 = request.POST['val4']

        OTP_receive = str(val1) + str(val2) + str(val3) + str(val4)

        # SESSION VALUES
        name = request.session['name']
        email = request.session['email']
        passwd = request.session['passwd']
        OTP_actual = request.session['OTP']

        if(str(OTP_receive) == str(OTP_actual)):
            #new_user = User.objects.create_user(name, email, passwd)
            #new_user.save()
            return HttpResponse("Registration successfull")
        else :
            return HttpResponse("Incorrect OTP!")

    return HttpResponse(request.session['email'])

def signup(request):
    if request.method == "POST":
        # RECEIVED VALUES
        name = request.POST['name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # OTP GENERATOR
        OTP = random.randint(1000, 9999)
        actual_message = 'Your Registration OTP is : ' + str(OTP)
        
        # SESSION VALUES
        request.session['name'] = name
        request.session['email'] = email
        request.session['passwd'] = pass1
        request.session['OTP'] = OTP

        # Mailing PROTOCOL
        send_mail(
            'OTP From SilverPay Community' , # Subject
            actual_message, # Message
            email , # From Email
            [email], # To Email
        )

        return render(request, 'login/OTP.html')
        
    return render(request, 'login/SignUp.html')

def home(request):
    return render(request, 'profile/index.html')

def profile(request):
    return HttpResponse('This is the profile page')


