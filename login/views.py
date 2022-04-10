from multiprocessing import context
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth import login as access
from django.core.mail import send_mail
from datetime import date, datetime
from .models import balance_data, trans_data, key_pair1, key_pair2, notification
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

def initial_transaction(request, amount):
    user = request.user

    cash_in(request, amount)

    new_entry = trans_data(owner=user, total_amount = 1.0, des1 = 'Welcome Money', des2 = 'SilverPay provides some initial amount for every account', tr_amount = amount, in_out = 'in')
    new_entry.save()
    return

def welcome_notification(request):
    user = request.user
    new_data = notification(user = user, subject = 'Congratulation, You made it!', description = 'Welcome to Silverpay, your account created successfully!')
    new_data.save()
    return

'''-------------------------------------- Start Three Way Transaction Protocol ---------------------------------------'''

def encrypt(public_key, plaintext):

    # Unpack the key into it's components
    key, n = public_key

    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
            
    numberRepr = [ord(char) for char in plaintext]
    # print("\nNumeric representation before encryption: ", numberRepr) # Run for development purpose
    cipher = [pow(ord(char),key,n) for char in plaintext]
    
    # Return the array of bytes
    return cipher


def decrypt(private_key, ciphertext):

    # Unpack the key into its components
    key, n = private_key
       
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    numberRepr = [pow(char, key, n) for char in ciphertext]
    plain = [chr(pow(char, key, n)) for char in ciphertext]

    # print("\nRestore numeric representation : ", numberRepr) # Run for development purpose
    
    # Return the array of bytes as a string
    return ''.join(plain)


def three_way_transaction_protocol(request, the_username):

    receiver = User.objects.get(username=the_username)

    # Fetch secret keys to perform secure transaction
    receiver_key_pair1 = key_pair1.objects.get(user=receiver)
    receiver_key_pair2 = key_pair2.objects.get(user=receiver)

    # Fetch values
    public_key1 = receiver_key_pair1.public_key
    private_key1 = receiver_key_pair1.private_key

    public_key2 = receiver_key_pair2.public_key
    private_key2 = receiver_key_pair2.public_key

    # Resolve Complexity
    public_key = (public_key1, public_key2)
    private_key = (private_key1, private_key2)

    chipher = encrypt(public_key, the_username)

    if(the_username == decrypt(private_key, chipher)):
        return 'pass'
    else:
        return 'fail'

def sending_money(request, the_username, amount):

    # SYSTEM --
    receiver = User.objects.get(username=the_username)
    sender = request.user
    
    receiver_balance = balance_data.objects.get(user=receiver)
    sender_balance = balance_data.objects.get(user=sender)

    # ---------- The three way transaction system phases --------------- #

    # Phase 1 - Ensure safe outgoing route
    value1 = three_way_transaction_protocol(request, the_username)

    if(value1 != 'pass'):
        return HttpResponse('Cannot ensure safe route for transaction')

    # Phase 2 - Ensure safe incoming route

    value2 = three_way_transaction_protocol(request, request.user.username)
    if(value2 != 'pass'):
        return HttpResponse('Cannot ensure safe route for transaction')

    # Phase 3 - Confirm the transaction

    receiver_balance.total_amount = receiver_balance.total_amount + amount
    sender_balance.total_amount = sender_balance.total_amount - amount
    
    receiver_balance.save()
    sender_balance.save()

    # Create the transaction description

    new_entry1 = trans_data(owner=receiver, total_amount = 1.0, des1 = 'Received money', des2 = 'You received money from ' + request.user.username, tr_amount = amount, in_out = 'in')
    new_entry1.save()

    new_entry2 = trans_data(owner=request.user, total_amount = 1.0, des1 = 'Send money', des2 = 'You send your money to ' + receiver.username, tr_amount = amount, in_out = 'out')
    new_entry2.save()


    return

'''--------------------------------------- End Three Way Transaction Protocol ----------------------------------------'''



''' ------------------------------------- Start BlockChain Protocol -------------------------------------------------'''
def coprime(a, b):
    while b != 0:
        a, b = b, a % b
    return a
    
def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

# Euclid's extended algorithm for finding the multiplicative inverse of two numbers    
def modinv(a, m):
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise Exception('Modular inverse does not exist')
	return x % m    


def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = p * q

    # Phi is the totient of n
    phi = (p-1) * (q-1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime 
    g = coprime(e, phi)
  
    while g != 1:
        e = random.randrange(1, phi)
        g = coprime(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = modinv(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False
                
        if isPrime:
            prime_list.append(n)
    return prime_list



def generate_keys(request, username):

    the_user = User.objects.get(username=username).pk

    key1 = key_pair1.objects.get(user= the_user)
    key2 = key_pair2.objects.get(user= the_user)

    prime_list = primesInRange(17,2000)
    p = random.choice(prime_list)

    prime_list = primesInRange(2001,5000)
    q = random.choice(prime_list)

    # Generating publice and private key for the user
    print(this_moment + " Generating your public/private keypairs")
    public_key, private_key = generate_keypair(p, q) 

    public_key1, public_key2 = public_key
    private_key1, private_key2 = private_key
    
    key1.public_key = public_key1
    key1.private_key = private_key1

    key2.public_key = public_key2
    key2.private_key = private_key2

    key1.save()
    key2.save()

    return

'''------------------------------------- End BlockChain Protocol ----------------------------------------------------'''

# All Views

def transactions(request):
    if request.user.is_authenticated:

        username = request.user.username
        context = {
            'username' : username,
            'transaction' : trans_data.objects.filter(owner=request.user.id).order_by("date").reverse(),
        }
        return render(request, 'profile/transactions.html', context)
    else:
        return render(request, 'profile/index.html')

def Transaction_OTP(request):
    if request.method == "POST":
        # OTP VALUE
        val1 = request.POST['val1']
        val2 = request.POST['val2']
        val3 = request.POST['val3']
        val4 = request.POST['val4']

        OTP_receive = str(val1) + str(val2) + str(val3) + str(val4)

        # SESSION VALUES
        OTP_actual = request.session['OTP']
        username = request.session['username']
        amount = request.session['amount']

        sender = request.user
        sender_balance = balance_data.objects.get(user=sender)

        if(sender_balance.total_amount < float(amount)):
            return HttpResponse("You dont have enough money!")

        if(str(OTP_receive) == str(OTP_actual)):

            context = {
                'username' : username,
                'amount' : amount
            }
            
            del request.session['OTP']
            sending_money(request, username, float(amount))
            del request.session['username']
            del request.session['amount']

            return render(request, 'profile/send-money-success.html', context)

        else:
            return HttpResponse("Incorrect OTP!")

    return redirect('home')

def send_money(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            username = request.POST['username']
            amount = request.POST['amount']

            # OTP GENERATOR
            OTP = random.randint(1000, 9999)
            actual_message = 'Your transaction confirmation OTP is : ' + str(OTP)
            email = request.user.email

            request.session['OTP'] = OTP
            request.session['username'] = username
            request.session['amount'] = amount
            

            # Mailing PROTOCOL
            send_mail(
                'OTP From SilverPay Community' , # Subject
                actual_message, # Message
                email , # From Email
                [email], # To Email
            )

            return render(request, 'login/Transaction_OTP.html')

        return render(request, 'profile/send-money.html')
    else:
        return render(request, 'profile/index.html')

def req_money(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            username = request.POST['username']
            amount = request.POST['amount']
            description = request.POST['description']

            context = {
                'username' : username,
                'amount' : amount
            }

            the_user = User.objects.get(username=username)
            new_data = notification(user = the_user, subject = 'Money request from, ' + request.user.username, description = description, username=username, amount=float(amount))
            new_data.save()

            return render(request, 'profile/request-money-success.html', context)

        return render(request, 'profile/request-money.html')
    else:
        return render(request, 'profile/index.html')


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

            balance_data.objects.create(user=user)
            notification.objects.create(user=user)
            key_pair1.objects.create(user=user)
            key_pair2.objects.create(user=user)

            
            if user is not None:
                if user.is_active:
                    access(request, user)
                    
                    # Generating kay pairs for new account
                    generate_keys(request, request.user.username)
                    
                    # Say Contgratulation to the new user
                    welcome_notification(request)

                    # Given some initial amount from SilverPay
                    initial_transaction(request, 1000.0)

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

        return render(request, 'profile/dashboard.html', context)
    else:
        return render(request, 'profile/index.html')

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile/profile.html')
    else:
        return render(request, 'profile/index.html')

def profile_notifications(request):
    if request.user.is_authenticated:
        context = {
            'notifications' : notification.objects.filter(user=request.user.id).order_by("date").reverse(),
        }

        return render(request, 'profile/profile-notifications.html', context)
    else:
        return render(request, 'profile/index.html')

def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


