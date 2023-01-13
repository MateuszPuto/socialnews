from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from django.core.mail import send_mail
from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from datetime import datetime

import random

from user.models import Secrets
from user.forms import CreateAccount, CheckPassword, ChangePassword

def create_account(request):
    if request.method == 'POST':
        form = CreateAccount(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            if data["password"] != data["confirm_password"]:
                raise Http404("Password needs to be identical.")

            new_user = User.objects.create_user(data["username"], email=data["email"], password=data["password"])
            new_user.first_name = data["first_name"]
            new_user.last_name = data["last_name"]
            new_user.save()

            messages.add_message(request, messages.INFO, f'Thanks {data["username"]} for registering on our site.')

            return render(request, 'user/messages.html')
    else:
        form = CreateAccount()

    return render(request, 'user/register.html', {'form': form})

@login_required(login_url='/accounts/login/')
def profile(request):
    if request.user.is_authenticated:
        context = {}
        context["username"] = request.user.get_username()
        context["fullname"] = request.user.get_full_name()
        context["email"] = request.user.email
        context["password"] = ""

        return render(request, 'user/profile.html', context)

@login_required(login_url='/accounts/login/')
def check_password_if_valid(request):
    user = request.user

    if request.method == 'POST':
        form = CheckPassword(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if user.check_password(raw_password=data["password"]):
                messages.add_message(request, messages.INFO, 'This is valid password.')

                return render(request, 'user/messages.html')
            else:
                messages.add_message(request, messages.WARNING, 'This is not a valid password.')

                return render(request, 'user/messages.html')
    else:
        form = CheckPassword()

    return render(request, 'user/checkpassword.html', {'form': form})

@login_required(login_url='/accounts/login/')
def recover_password(request):
    secret = ""
    for i in range(4):
        secret += str(random.randrange(9))

    Secrets.objects.filter(username=request.user).delete()
    Secrets.objects.create(username=request.user, secret=secret)

    send_mail(
    'Socialnews password recovery',
    f'Hello,\nyou have requested to recover your password. Your secret is: {secret}.\
    Go to https://socialnews.com/forum/ to create new safe password.\
    Please keep your password safe. If you expect that somebody may have come in possesion of your password\
    please change it immediately.\n\nBest regards,\nSocialnews',
    'socialnews@example.com',
    [request.user.email],
    fail_silently=False,
    )

    return HttpResponseRedirect(reverse('user:profile'))

@login_required(login_url='/accounts/login/')
def change_password(request):
    if request.method == 'POST':
        form = ChangePassword(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            new_password = data["password"]
            user_secret = data["secret"]

            secret = Secrets.objects.get(username=request.user.get_username()).secret

            if user_secret == secret:
                user = request.user
                user.set_password(new_password)
                user.save()
            else:
                raise Http404("Incorrect secret provided.")
        else:
            raise Http404("Form input not valid.")
    else:
        form = ChangePassword()

        return render(request, 'user/changepassword.html', {'form': form})
