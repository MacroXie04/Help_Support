from django.contrib.auth import login
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required
from account.models import UserProfile, AccountBalance
from django.utils import timezone
from django.contrib.auth import logout


def web_login(request):
    return render(request, 'login.html')


def web_register(request):
    return render(request, 'register.html')


def web_account_page(request):
    if not request.user.userprofile.is_active:
        return redirect('account_disabled')
    else:
        return render(request, 'account_page/account_page.html')


@login_required(login_url='/account/login/')
def web_logout(request):
    logout(request)
    return redirect('login')


def web_account_disable(request):
    if request.user.userprofile.is_active:
        return redirect('index')
    else:
        return render(request, 'account_page/account_disabled.html')
