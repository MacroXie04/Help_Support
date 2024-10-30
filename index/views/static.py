from django.contrib.auth import login
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.template.context_processors import request
from account.models import UserProfile, AccountBalance
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required(login_url='/account/login/')
def index(request):
    return render(request, 'index/index_help.html')



