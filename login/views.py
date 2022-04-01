from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth import login as access
from django.core.mail import send_mail
from datetime import date, datetime
from .models import balance_data, trans_data
import random


# Time Formatting for console
today = date.today()
now = datetime.now()
	
current_date = today.strftime("%d/%b/%Y")
current_time = now.strftime("%H:%M:%S")

this_moment = '[' + current_date + ' ' + current_time + ']'

# Protocols
def cash_in(request, amount):

    # SYSTEM --
    user = request.user
    user_current_balance = balance_data.objects.get(user=user)
    user_current_balance.total_amount = user_current_balance.total_amount + amount
    user_current_balance.save()
    return    
    

def cash_out(request, amount):

    # SYSTEM --
    user = request.user
    user_current_balance = balance_data.objects.get(user=user)
    user_current_balance.total_amount = user_current_balance.total_amount - amount
    user_current_balance.save()
    return

def send_money(request, the_username, amount):

    # SYSTEM --
    the_user = User.objects.get(username=the_username).pk
    user_current_balance = balance_data.objects.get(user= the_user)

    return HttpResponse(user_current_balance.total_amount)


# All Views
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(this_moment + ' Fetch the login data')
        user = authenticate(username = username, password = password)
        if user is not None:
            print(this_moment + ' Sending to the kerberos authentication system')
            if user.is_active:
                access(request, user)
                print(this_moment + ' Authentication sucessful')
                return redirect('home')
        else:
            print(this_moment + ' Invalid authentication')
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

        username = request.user.username
        context = {
            'username' : username,
            'transaction' : trans_data.objects.filter(owner=request.user.id).order_by("date").reverse(),
        }
        # cash_in(request, 12.0)
        a_username = 'mehedi'
        a_user = User.objects.get(username=a_username).pk

        user_current_balance = balance_data.objects.get(user= a_user)

        return HttpResponse(user_current_balance.total_amount)


        # return render(request, 'profile/dashboard.html', context)
    else:
        return render(request, 'profile/index.html')

def profile(request):
    return render(request, 'profile/profile.html')

def profile_notifications(request):
    return render(request, 'profile/profile-notifications.html')

def transactions(request):
    return render(request, 'profile/transactions.html')

def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponse('Signout Successfull!')


