"""SilverPay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.urls import path
from login import views as login_view

urlpatterns = [
    path('signup/', login_view.signup, name='signup'),
    path('login/', login_view.login, name='login'),
    path('OTP/', login_view.OTP, name='OTP'),
    path('trans-OTP/', login_view.Transaction_OTP, name='trans-OTP'),
    path('', login_view.home, name='home'),
    path('send-money/', login_view.send_money, name='send-money'),
    path('req-money/', login_view.req_money, name='req-money'),
    path('profile/', login_view.profile, name='profile'),
    path('profile-notifications/', login_view.profile_notifications, name='profile-notifications'),
    path('transactions/', login_view.transactions, name='transactions'),
    path('logout/', login_view.signout, name='logout'),
    path('admin/', admin.site.urls),
]
