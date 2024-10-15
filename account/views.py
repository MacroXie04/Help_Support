from .forms import UserRegisterForm, UserLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout


def account_disabled(request):
    if request.user.is_active:
        return redirect('index')
    else:
        return render(request, 'account_disabled.html')

@login_required(login_url='/account/login/')
def web_logout(request):
    logout(request)
    return redirect('login')

def web_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def web_register(request):
    if request.method == 'POST':
        web_register_form = UserRegisterForm(request.POST)
        if web_register_form.is_valid():
            user = web_register_form.save()
            login(request, user)
            messages.success(request, "register success")
            return redirect('index')
    else:
        web_register_form = UserRegisterForm()
    return render(request, 'register.html', {'form': web_register_form})

