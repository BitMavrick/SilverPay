from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as access
from django.core.mail import send_mail
import random

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                access(request, user)
                return redirect('home')
        else:
            return HttpResponse('Wrong username or password!')
        
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
        username = request.session['username']
        email = request.session['email']
        passwd = request.session['passwd']
        OTP_actual = request.session['OTP']

        if(str(OTP_receive) == str(OTP_actual)):
            new_user = User.objects.create_user(username, email, passwd)
            new_user.save()

            del request.session['username']
            del request.session['email']
            del request.session['passwd']
            del request.session['OTP']

            user = authenticate(username = username, password = passwd)
            if user is not None:
                if user.is_active:
                    access(request, user)
                    return redirect('home')
            else:
                return HttpResponse("Incorrect OTP!")

    return redirect('home')

def signup(request):
    if request.method == "POST":
        # RECEIVED VALUES
        username = request.POST['name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # OTP GENERATOR
        OTP = random.randint(1000, 9999)
        actual_message = 'Your Registration OTP is : ' + str(OTP)
        
        # SESSION VALUES
        request.session['username'] = username
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
    if request.user.is_authenticated:
        return render(request, 'profile/dashboard.html')
    else:
        return render(request, 'profile/index.html')

def profile(request):
    return HttpResponse('This is the profile page')

def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponse('Signout Successfull!')


