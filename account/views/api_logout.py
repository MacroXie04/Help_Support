from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required(login_url='/account/login/')
def api_logout(request):
    logout(request)
    return redirect('login')
